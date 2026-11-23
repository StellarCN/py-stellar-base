"""
SEP: 0007
Title: URI Scheme to facilitate delegated signing
Author: Nikhil Saraf (Lightyear.io / SDF)
Status: Active
Created: 2018-05-07
Updated: 2020-07-29
Version: 2.1.0
"""

import base64
import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from decimal import Decimal
from typing import ClassVar, Final, Self
from urllib.parse import quote, unquote_plus, urlencode

from ..asset import Asset
from ..exceptions import BadSignatureError
from ..fee_bump_transaction_envelope import FeeBumpTransactionEnvelope
from ..keypair import Keypair
from ..memo import HashMemo, IdMemo, Memo, NoneMemo, ReturnHashMemo, TextMemo
from ..network import Network
from ..strkey import Contract, Ed25519PublicKey, MuxedContract, MuxedEd25519Account
from ..transaction_builder import TransactionBuilder
from ..transaction_envelope import TransactionEnvelope
from ..utils import to_xdr_amount
from .exceptions import InvalidStellarUriError

__all__ = [
    "PayStellarUri",
    "Replacement",
    "TransactionStellarUri",
    "parse_stellar_uri",
]

# A signature covers the text of a URI, not its fields. So a URI object holds its
# text, which never changes, and its fields are read from that text. A constructor
# writes its arguments as a URI and reads it with the parser that reads a received
# one. An object's fields therefore always agree with its text, the SDK can read
# whatever it writes, and a received URI verifies against the very bytes its sender
# signed, however the sender ordered or encoded the parameters.

STELLAR_SCHEME: str = "web+stellar"
_PREFIX: Final = f"{STELLAR_SCHEME}:"
# What a signer puts before the text it signs.
_SIGNATURE_PAYLOAD_PREFIX: Final = bytes(35) + b"\x04" + b"stellar.sep.7 - URI Scheme"
_SIGNATURE_LENGTH: Final = 64
_MAX_MESSAGE_LENGTH: Final = 300
_MEMO_TYPES: Final = ("MEMO_TEXT", "MEMO_ID", "MEMO_HASH", "MEMO_RETURN")
# An amount has 7 decimal places at most, so any that matches is exact in stroops.
_AMOUNT: Final = re.compile(r"[0-9]+(\.[0-9]{1,7})?")
# SEP-0002: a federation name is printable, without whitespace, `*` or `>`.
_FEDERATION_NAME: Final = re.compile(r"[^\s*>]+")
_MEMO_ID: Final = re.compile(r"[0-9]+")
_DOMAIN_LABEL: Final = re.compile(r"[A-Za-z0-9]([A-Za-z0-9-]*[A-Za-z0-9])?")
# Txrep's `_present` of an optional value and `len` of an array, which aren't values
# of the transaction: setting one would add or remove what the user never saw.
_METADATA_SUFFIXES: Final = ("._present", ".len")


@dataclass(frozen=True, kw_only=True)
class Replacement:
    """A value the wallet asks the user for, and where it goes in the transaction.

    An example::

        Replacement(
            identifier="X",
            hint="account that pays the fee",
            fields=["sourceAccount", "operations[0].sourceAccount"],
        )

    See `SEP-0007 <https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0007.md#operation-tx>`__

    :param identifier: A name for the value, which ties the fields to the hint.
    :param hint: What the wallet tells the user about the value. It can't contain a
        comma, which SEP-0007 uses between two hints and has no way to escape.
    :param fields: The fields of the transaction the value replaces, by their Txrep
        (SEP-0011) names without the ``tx.`` prefix, such as ``sourceAccount``.
    :raises: :exc:`InvalidStellarUriError <stellar_sdk.sep.exceptions.InvalidStellarUriError>`:
        if the values can't be written in a URI.
    """

    identifier: str
    hint: str
    fields: Sequence[str]

    def __post_init__(self) -> None:
        if isinstance(self.fields, str):
            raise TypeError("`fields` is a sequence of field names, not a string.")
        object.__setattr__(self, "fields", tuple(self.fields))
        if not self.identifier or not self.fields or not all(self.fields):
            raise InvalidStellarUriError(
                "A replacement needs an identifier and fields."
            )
        for name in (self.identifier, *self.fields):
            if any(separator in name for separator in ":,;"):
                raise InvalidStellarUriError(
                    "An identifier or a field of a replacement can't contain "
                    f"`:`, `,` or `;`: {name!r}"
                )
        for name in self.fields:
            if name.endswith(_METADATA_SUFFIXES):
                raise InvalidStellarUriError(
                    f"`replace` can't name the field {name!r}, which isn't a value "
                    "of the transaction."
                )
        if "," in self.hint:
            raise InvalidStellarUriError(f"A hint can't contain `,`: {self.hint!r}")


class _StellarUri:
    """What the two kinds of URI share: their text, and its signature."""

    _operation: ClassVar[str]
    _parameters: ClassVar[frozenset[str]]
    callback: str | None
    message: str | None
    network_passphrase: str
    origin_domain: str | None
    signature: str | None
    _uri: str

    @classmethod
    def from_uri(cls, uri: str) -> Self:
        """Read a URI.

        Parameters may come in any order. Those the SDK doesn't know are left in
        the text, so the signature still verifies, but a parameter it knows can't
        be given twice, and an empty value is a value, not a missing one.

        :param uri: The URI.
        :return: The request the URI makes.
        :raises: :exc:`InvalidStellarUriError <stellar_sdk.sep.exceptions.InvalidStellarUriError>`:
            if the text is not a valid URI of this kind; the message names the
            parameter.
        """
        self = object.__new__(cls)
        self._load(uri)
        return self

    def to_uri(self) -> str:
        """The text of the URI, which is the received one if the URI was read.

        :return: The URI.
        """
        return self._uri

    def sign(self, signer: Keypair | str, origin_domain: str) -> Self:
        """Sign the URI for a domain, which a wallet shows the user as the origin.

        The object doesn't change. The URI of the returned one has
        ``origin_domain`` and ``signature`` at its end, in place of any it had.

        :param signer: The keypair or the secret seed of the
            ``URI_REQUEST_SIGNING_KEY`` in the stellar.toml of the domain.
        :param origin_domain: The fully qualified domain name of the origin.
        :return: The signed URI.
        :raises: :exc:`InvalidStellarUriError <stellar_sdk.sep.exceptions.InvalidStellarUriError>`:
            if ``origin_domain`` is not a domain name.
        """
        if isinstance(signer, str):
            signer = Keypair.from_secret(signer)
        operation, pairs = _split(self._uri)
        kept = [
            raw for raw, name, _ in pairs if name not in {"origin_domain", "signature"}
        ]
        domain = quote(origin_domain, safe="")
        text = f"{_PREFIX}{operation}?{'&'.join(kept)}&origin_domain={domain}"
        signature = signer.sign(_SIGNATURE_PAYLOAD_PREFIX + text.encode())
        encoded = quote(base64.b64encode(signature).decode(), safe="")
        return self.from_uri(f"{text}&signature={encoded}")

    def verify_signature(self, signing_key: str) -> None:
        """Verify the signature of the URI, which covers its text as it was read.

        The SDK doesn't fetch the key, so that the wallet can compare it with the
        one it knows for the domain, as SEP-0007 asks. It is in the stellar.toml
        of :attr:`origin_domain`::

            toml = fetch_stellar_toml(uri.origin_domain)
            uri.verify_signature(toml["URI_REQUEST_SIGNING_KEY"])

        :param signing_key: The ``URI_REQUEST_SIGNING_KEY`` of the origin domain.
        :raises: :exc:`BadSignatureError <stellar_sdk.exceptions.BadSignatureError>`:
            if the URI isn't signed, ``signing_key`` isn't a public key, or the
            signature isn't one of the key.
        """
        if self.signature is None:
            raise BadSignatureError("The URI is not signed.")
        try:
            signature = base64.b64decode(self.signature, validate=True)
        except ValueError:
            signature = b""
        if len(signature) != _SIGNATURE_LENGTH:
            raise BadSignatureError(
                "The `signature` of the URI is not a signature: 64 bytes in base64."
            )
        operation, pairs = _split(self._uri)
        unsigned = "&".join(raw for raw, name, _ in pairs if name != "signature")
        payload = (
            _SIGNATURE_PAYLOAD_PREFIX + f"{_PREFIX}{operation}?{unsigned}".encode()
        )
        try:
            keypair = Keypair.from_public_key(signing_key)
        except ValueError as e:
            # The key comes from a stellar.toml, which may hold anything.
            raise BadSignatureError("`signing_key` is not a public key.") from e
        keypair.verify(payload, signature)

    def _load(self, uri: str) -> None:
        """Set the fields from a URI."""
        operation, pairs = _split(uri)
        if operation != self._operation:
            raise InvalidStellarUriError(
                f"The URI is not a `{self._operation}` request."
            )
        params: dict[str, str] = {}
        for _, name, value in pairs:
            if name in self._parameters:
                if name in params:
                    raise InvalidStellarUriError(f"`{name}` is given more than once.")
                params[name] = value
        callback = params.get("callback")
        if callback is not None:
            if not callback.startswith("url:") or callback == "url:":
                raise InvalidStellarUriError(
                    "`callback` must be `url:` followed by a URL."
                )
            callback = callback.removeprefix("url:")
        message = params.get("msg")
        if message is not None and len(message) > _MAX_MESSAGE_LENGTH:
            raise InvalidStellarUriError(
                f"`msg` is longer than {_MAX_MESSAGE_LENGTH} characters."
            )
        network_passphrase = params.get(
            "network_passphrase", Network.PUBLIC_NETWORK_PASSPHRASE
        )
        if not network_passphrase:
            raise InvalidStellarUriError("`network_passphrase` is empty.")
        origin_domain, signature = params.get("origin_domain"), params.get("signature")
        if (origin_domain is None) != (signature is None):
            # A domain that nothing vouches for, or a signature of no one.
            raise InvalidStellarUriError(
                "`origin_domain` and `signature` must be given together."
            )
        if origin_domain is not None and not _is_domain_name(origin_domain):
            raise InvalidStellarUriError(
                f"`origin_domain` is not a domain name: {origin_domain!r}"
            )
        self._set(
            _uri=uri,
            callback=callback,
            message=message,
            network_passphrase=network_passphrase,
            origin_domain=origin_domain,
            signature=signature,
        )
        self._read(params)

    def _read(self, params: Mapping[str, str]) -> None:
        """Set the fields of the kind from its parameters."""
        raise NotImplementedError

    def _set(self, **values: object) -> None:
        for name, value in values.items():
            object.__setattr__(self, name, value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, _StellarUri):
            return NotImplemented
        return self._uri == other._uri

    def __hash__(self) -> int:
        return hash(self._uri)


@dataclass(frozen=True, init=False, eq=False, match_args=False)
class PayStellarUri(_StellarUri):
    """A request to pay a destination, for a wallet to make a transaction of.

    The object can't be changed. It holds the text of its URI, which
    :meth:`to_uri` returns, and two objects are equal when their texts are. To
    compare what two URIs ask for, compare their attributes.

    Each parameter below is an attribute too, read from the URI: ``amount`` is its
    text, and ``asset`` and ``memo`` are never ``None`` but the native asset and a
    :class:`NoneMemo <stellar_sdk.memo.NoneMemo>`. ``origin_domain`` and
    ``signature`` are ``None`` until the URI is signed with :meth:`sign`, or unless
    a URI read with :meth:`from_uri` has them.

    See `SEP-0007 <https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0007.md#operation-pay>`__

    :param destination: The account, the contract or the federation address
        (``name*example.com``) to pay.
    :param amount: The amount the destination receives. Without one, the wallet
        asks the user for it.
    :param asset: The asset the destination receives, the native one by default.
    :param memo: The memo of the payment. A contract can't be paid with one.
    :param callback: The URL the wallet sends the signed transaction to, instead
        of to the network.
    :param message: What the wallet tells the user about the request, in 300
        characters at most.
    :param network_passphrase: The network of the payment, the public one by
        default.
    :raises: :exc:`InvalidStellarUriError <stellar_sdk.sep.exceptions.InvalidStellarUriError>`:
        if a value can't be written in a URI.
    """

    _operation: ClassVar[str] = "pay"
    _parameters: ClassVar[frozenset[str]] = frozenset(
        {
            "destination",
            "amount",
            "asset_code",
            "asset_issuer",
            "memo",
            "memo_type",
            "callback",
            "msg",
            "network_passphrase",
            "origin_domain",
            "signature",
        }
    )
    destination: str
    amount: str | None
    asset: Asset
    memo: Memo
    callback: str | None
    message: str | None
    network_passphrase: str
    origin_domain: str | None
    signature: str | None
    _uri: str = field(repr=False)

    def __init__(
        self,
        destination: str,
        *,
        amount: str | Decimal | None = None,
        asset: Asset | None = None,
        memo: Memo | None = None,
        callback: str | None = None,
        message: str | None = None,
        network_passphrase: str = Network.PUBLIC_NETWORK_PASSPHRASE,
    ) -> None:
        if isinstance(amount, Decimal):
            amount = format(amount, "f")
        code = issuer = None
        if asset is not None and not asset.is_native():
            code, issuer = asset.code, asset.issuer
        memo_value, memo_type = _write_memo(memo)
        self._load(
            _write(
                self._operation,
                {
                    "destination": destination,
                    "amount": amount,
                    "asset_code": code,
                    "asset_issuer": issuer,
                    "memo": memo_value,
                    "memo_type": memo_type,
                    "callback": _write_callback(callback),
                    "msg": message,
                    "network_passphrase": _write_network(network_passphrase),
                },
            )
        )

    def _read(self, params: Mapping[str, str]) -> None:
        destination = params.get("destination")
        if destination is None:
            raise InvalidStellarUriError("`destination` is missing.")
        contract = Contract.is_valid(destination) or MuxedContract.is_valid(destination)
        if not (
            contract
            or Ed25519PublicKey.is_valid(destination)
            or MuxedEd25519Account.is_valid(destination)
            or _is_federation_address(destination)
        ):
            raise InvalidStellarUriError(
                "`destination` is not an account, a contract or a federation "
                f"address: {destination!r}"
            )
        amount = params.get("amount")
        if amount is not None:
            _check_amount(amount)
        memo = _read_memo(params.get("memo"), params.get("memo_type"))
        if contract and not isinstance(memo, NoneMemo):
            # A wallet could only drop the memo, and pay without it.
            raise InvalidStellarUriError(
                "`memo` can't be given with a contract `destination`, which is "
                "paid by a Soroban transaction, and those have no memo."
            )
        self._set(
            destination=destination,
            amount=amount,
            asset=_read_asset(params.get("asset_code"), params.get("asset_issuer")),
            memo=memo,
        )


@dataclass(frozen=True, init=False, eq=False, match_args=False)
class TransactionStellarUri(_StellarUri):
    """A request to sign a transaction.

    The object can't be changed. It holds the text of its URI, which
    :meth:`to_uri` returns, and two objects are equal when their texts are. To
    compare what two URIs ask for, compare their attributes.

    The transaction is kept as ``xdr``, the base64 of the envelope as it was when
    the object was made: signing the envelope afterwards doesn't change the URI.
    A wallet gets an envelope to sign from :meth:`to_transaction_envelope`.

    The other attributes are ``network_passphrase`` and the parameters below,
    with ``replace`` as a tuple. ``origin_domain`` and ``signature`` are ``None``
    until the URI is signed with :meth:`sign`, or unless a URI read with
    :meth:`from_uri` has them.

    See `SEP-0007 <https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0007.md#operation-tx>`__

    :param transaction_envelope: The transaction to sign. The URI is for its
        network.
    :param replace: The values the wallet asks the user for, and the fields of
        the transaction they replace.
    :param callback: The URL the wallet sends the signed transaction to, instead
        of to the network.
    :param pubkey: The account the wallet should sign for.
    :param chain: The URI this one was made from, as its text. Read it with
        :func:`parse_stellar_uri`; SEP-0007 has it for information only.
    :param message: What the wallet tells the user about the request, in 300
        characters at most.
    :raises: :exc:`InvalidStellarUriError <stellar_sdk.sep.exceptions.InvalidStellarUriError>`:
        if a value can't be written in a URI.
    """

    _operation: ClassVar[str] = "tx"
    _parameters: ClassVar[frozenset[str]] = frozenset(
        {
            "xdr",
            "replace",
            "callback",
            "pubkey",
            "chain",
            "msg",
            "network_passphrase",
            "origin_domain",
            "signature",
        }
    )
    xdr: str
    replace: tuple[Replacement, ...]
    callback: str | None
    pubkey: str | None
    chain: str | None
    message: str | None
    network_passphrase: str
    origin_domain: str | None
    signature: str | None
    _uri: str = field(repr=False)

    def __init__(
        self,
        transaction_envelope: TransactionEnvelope | FeeBumpTransactionEnvelope,
        *,
        replace: Iterable[Replacement] = (),
        callback: str | None = None,
        pubkey: str | None = None,
        chain: str | None = None,
        message: str | None = None,
    ) -> None:
        self._load(
            _write(
                self._operation,
                {
                    "xdr": transaction_envelope.to_xdr(),
                    "callback": _write_callback(callback),
                    "replace": _write_replace(replace),
                    "pubkey": pubkey,
                    "chain": chain,
                    "msg": message,
                    "network_passphrase": _write_network(
                        transaction_envelope.network_passphrase
                    ),
                },
            )
        )

    def to_transaction_envelope(
        self,
    ) -> TransactionEnvelope | FeeBumpTransactionEnvelope:
        """The transaction to sign, as a new envelope each time.

        :return: The envelope of ``xdr``, for the network of the URI.
        """
        return TransactionBuilder.from_xdr(self.xdr, self.network_passphrase)

    def _read(self, params: Mapping[str, str]) -> None:
        xdr = params.get("xdr")
        if xdr is None:
            raise InvalidStellarUriError("`xdr` is missing.")
        self._set(xdr=xdr)
        try:
            self.to_transaction_envelope()
        except ValueError as e:
            raise InvalidStellarUriError(
                f"`xdr` is not a transaction envelope: {e}"
            ) from e
        pubkey = params.get("pubkey")
        if pubkey is not None and not Ed25519PublicKey.is_valid(pubkey):
            raise InvalidStellarUriError(f"`pubkey` is not an account: {pubkey!r}")
        chain = params.get("chain")
        if chain is not None and not chain.startswith(_PREFIX):
            raise InvalidStellarUriError(f"`chain` is not a `{_PREFIX}` URI.")
        replace = params.get("replace")
        self._set(
            replace=() if replace is None else _read_replace(replace),
            pubkey=pubkey,
            chain=chain,
        )


def parse_stellar_uri(uri: str) -> PayStellarUri | TransactionStellarUri:
    """Read a URI of either kind, as a wallet does that is handed one.

    An example::

        match parse_stellar_uri(text):
            case PayStellarUri() as pay:
                ...
            case TransactionStellarUri() as tx:
                ...

    :param uri: The URI.
    :return: A :class:`PayStellarUri` or a :class:`TransactionStellarUri`.
    :raises: :exc:`InvalidStellarUriError <stellar_sdk.sep.exceptions.InvalidStellarUriError>`:
        if the text is not a valid URI; the message names the parameter.
    """
    operation, _ = _split(uri)
    if operation == PayStellarUri._operation:
        return PayStellarUri.from_uri(uri)
    if operation == TransactionStellarUri._operation:
        return TransactionStellarUri.from_uri(uri)
    raise InvalidStellarUriError("The URI is neither a `pay` nor a `tx` request.")


def _split(uri: str) -> tuple[str, list[tuple[str, str, str]]]:
    """The operation of a URI and its parameters: each as written, then its decoded
    name and value."""
    if not uri.startswith(_PREFIX):
        raise InvalidStellarUriError(f"The URI doesn't start with `{_PREFIX}`.")
    if "#" in uri:
        # What follows would be a fragment, which a parameter can't be in.
        raise InvalidStellarUriError("The URI has a `#`, which is written `%23`.")
    operation, _, query = uri.removeprefix(_PREFIX).partition("?")
    pairs: list[tuple[str, str, str]] = []
    for raw in query.split("&"):
        name, _, value = raw.partition("=")
        try:
            pairs.append(
                (
                    raw,
                    unquote_plus(name, errors="strict"),
                    unquote_plus(value, errors="strict"),
                )
            )
        except UnicodeDecodeError as e:
            raise InvalidStellarUriError(
                f"The URI is not UTF-8 when its percent-encoding is decoded: {raw!r}"
            ) from e
    return operation, pairs


def _write(operation: str, params: Mapping[str, str | None]) -> str:
    """Write a URI, leaving out the parameters that are None."""
    given = {name: value for name, value in params.items() if value is not None}
    return f"{_PREFIX}{operation}?{urlencode(given, quote_via=quote)}"


def _write_callback(callback: str | None) -> str | None:
    return None if callback is None else f"url:{callback}"


def _write_network(network_passphrase: str) -> str | None:
    """A URI without `network_passphrase` is for the public network."""
    if network_passphrase == Network.PUBLIC_NETWORK_PASSPHRASE:
        return None
    return network_passphrase


def _is_domain_name(text: str) -> bool:
    """Whether a text is a fully qualified domain name, which a wallet fetches the
    stellar.toml of: not a host name alone, an IP address, a port or a path.

    An internationalized name and a final dot are fine.
    """
    try:
        labels = text.removesuffix(".").encode("idna").decode().split(".")
    except UnicodeError:
        return False
    return (
        len(labels) > 1
        and all(_DOMAIN_LABEL.fullmatch(label) for label in labels)
        # No top-level domain starts with a digit, but the last part of an IP
        # address does, in whatever base it is written: `127.1`, `1.0x7f`.
        and not labels[-1][0].isdigit()
    )


def _is_federation_address(text: str) -> bool:
    name, _, domain = text.partition("*")
    return (
        bool(_FEDERATION_NAME.fullmatch(name))
        and name.isprintable()
        and _is_domain_name(domain)
    )


def _check_amount(amount: str) -> None:
    if not _AMOUNT.fullmatch(amount):
        raise InvalidStellarUriError(
            f"`amount` is not a number with at most 7 decimal places: {amount!r}"
        )
    try:
        stroops = to_xdr_amount(amount)
    except ValueError as e:
        raise InvalidStellarUriError(f"`amount` is invalid: {e}") from e
    if not stroops:
        raise InvalidStellarUriError("`amount` must be above zero.")


def _read_asset(code: str | None, issuer: str | None) -> Asset:
    if code is None:
        if issuer is not None:
            # Not an asset whose code is XLM: a wallet would show the native one.
            raise InvalidStellarUriError(
                "`asset_issuer` is given without `asset_code`."
            )
        return Asset.native()
    try:
        return Asset(code, issuer)
    except ValueError as e:
        raise InvalidStellarUriError(
            f"`asset_code` or `asset_issuer` is invalid: {e}"
        ) from e


def _write_memo(memo: Memo | None) -> tuple[str | None, str | None]:
    """The `memo` and the `memo_type` of a memo."""
    match memo:
        case None | NoneMemo():
            return None, None
        case TextMemo():
            try:
                return memo.memo_text.decode(), "MEMO_TEXT"
            except UnicodeDecodeError as e:
                raise InvalidStellarUriError(
                    "A text memo that isn't UTF-8 can't be written to a URI."
                ) from e
        case IdMemo():
            return str(memo.memo_id), "MEMO_ID"
        case HashMemo():
            return base64.b64encode(memo.memo_hash).decode(), "MEMO_HASH"
        case ReturnHashMemo():
            return base64.b64encode(memo.memo_return).decode(), "MEMO_RETURN"
        case _:
            raise TypeError(f"`memo` must be a Memo, not {type(memo).__name__}.")


def _read_memo(value: str | None, memo_type: str | None) -> Memo:
    if value is None:
        if memo_type is not None:
            raise InvalidStellarUriError("`memo_type` is given without `memo`.")
        return NoneMemo()
    if memo_type is None:
        # SEP-0007 names no default, and other SDKs write text memos this way.
        memo_type = "MEMO_TEXT"
    if memo_type not in _MEMO_TYPES:
        raise InvalidStellarUriError(f"`memo_type` is not a memo type: {memo_type!r}")
    try:
        if memo_type == "MEMO_TEXT":
            return TextMemo(value)
        if memo_type == "MEMO_ID":
            if not _MEMO_ID.fullmatch(value):
                raise ValueError("it must be an unsigned integer")
            return IdMemo(int(value))
        hash_value = base64.b64decode(value, validate=True)
        if memo_type == "MEMO_HASH":
            return HashMemo(hash_value)
        return ReturnHashMemo(hash_value)
    except ValueError as e:
        raise InvalidStellarUriError(f"`memo` is not a valid {memo_type}: {e}") from e


def _write_replace(replace: Iterable[Replacement]) -> str | None:
    replace = tuple(replace)
    if not replace:
        return None
    fields = ",".join(f"{name}:{r.identifier}" for r in replace for name in r.fields)
    hints = ",".join(f"{r.identifier}:{r.hint}" for r in replace)
    return f"{fields};{hints}"


def _read_replace(value: str) -> tuple[Replacement, ...]:
    """Read `field:identifier,...;identifier:hint,...`.

    SEP-0007 has no way to escape the separators. A field and an identifier can't
    contain them, so a hint is what follows the first colon of its entry, and may
    hold colons and semicolons, but not a comma.
    """
    fields_part, semicolon, hints_part = value.partition(";")
    if not semicolon:
        raise InvalidStellarUriError(
            "`replace` has no `;` between its fields and its hints."
        )
    hints: dict[str, str] = {}
    for entry in hints_part.split(","):
        identifier, colon, hint = entry.partition(":")
        if not colon:
            raise InvalidStellarUriError(f"`replace` has an invalid hint: {entry!r}")
        if identifier in hints:
            raise InvalidStellarUriError(
                f"`replace` gives the identifier {identifier!r} more than one hint."
            )
        hints[identifier] = hint
    fields: dict[str, list[str]] = {}
    names: set[str] = set()
    for entry in fields_part.split(","):
        name, colon, identifier = entry.partition(":")
        if not colon:
            raise InvalidStellarUriError(f"`replace` has an invalid field: {entry!r}")
        if name in names:
            raise InvalidStellarUriError(
                f"`replace` names the field {name!r} more than once."
            )
        names.add(name)
        fields.setdefault(identifier, []).append(name)
    if fields.keys() != hints.keys():
        raise InvalidStellarUriError(
            "`replace` must have the same identifiers on both sides of its `;`."
        )
    return tuple(
        Replacement(identifier=identifier, hint=hints[identifier], fields=names)
        for identifier, names in fields.items()
    )
