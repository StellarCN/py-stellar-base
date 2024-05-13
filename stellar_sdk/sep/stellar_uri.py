"""
SEP: 0007
Title: URI Scheme to facilitate delegated signing
Author: Nikhil Saraf (Lightyear.io / SDF)
Status: Active
Created: 2018-05-07
Updated: 2020-03-03
Version: 2.0.0
"""

import abc
import base64
from decimal import Decimal
from typing import Dict, List, Optional, Tuple, Union
from urllib import parse

from ..asset import Asset
from ..fee_bump_transaction_envelope import FeeBumpTransactionEnvelope
from ..keypair import Keypair
from ..memo import HashMemo, IdMemo, Memo, NoneMemo, ReturnHashMemo, TextMemo
from ..transaction_envelope import TransactionEnvelope

__all__ = ["PayStellarUri", "TransactionStellarUri", "Replacement"]

STELLAR_SCHEME: str = "web+stellar"


class StellarUri(object, metaclass=abc.ABCMeta):
    def __init__(self, signature: Optional[str] = None):
        self.signature = signature

    @abc.abstractmethod
    def to_uri(self) -> str:
        raise NotImplementedError("The method has not been implemented.")

    @property
    def _signature_payload(self) -> bytes:
        data = self.to_uri()
        if self.signature:
            data = data[: data.find("&signature=")]
        # https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0007.md#request-signing
        sign_data = b"\0" * 35 + b"\4" + b"stellar.sep.7 - URI Scheme" + data.encode()
        return sign_data

    def sign(self, signer: Union[Keypair, str]) -> None:
        """Sign the URI.

        :param signer: The account used to sign this transaction, it should be the secret key of `URI_REQUEST_SIGNING_KEY`.
        """
        if isinstance(signer, str):
            signer = Keypair.from_secret(signer)
        sign_data = self._signature_payload
        signature = signer.sign(sign_data)
        self.signature = base64.b64encode(signature).decode()

    @staticmethod
    def _parse_uri_query(uri_query) -> Dict[str, str]:
        return dict(parse.parse_qsl(uri_query))

    @staticmethod
    def _parse_callback(callback: Optional[str]) -> Optional[str]:
        if callback is None:
            return None
        if not callback.startswith("url:"):
            raise ValueError("`callback` should start with `url:`.")
        return callback[4:]


class PayStellarUri(StellarUri):
    """A request for a payment to be signed.

    See `SEP-0007 <https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0007.md#operation-pay>`_

    :param destination: A valid account ID or payment address.
    :param amount: Amount that destination will receive.
    :param asset: Asset destination will receive.
    :param memo: A memo to attach to the transaction.
    :param callback: The uri to post the transaction to after signing.
    :param message: An message for displaying to the user.
    :param network_passphrase: The passphrase of the target network.
    :param origin_domain: A fully qualified domain name that specifies the originating domain of the URI request.
    :param signature: A base64 encode signature of the hash of the URI request.
    """

    def __init__(
        self,
        destination: str,
        amount: Union[str, Decimal, None] = None,
        asset: Optional[Asset] = None,
        memo: Optional[Memo] = None,
        callback: Optional[str] = None,
        message: Optional[str] = None,
        network_passphrase: Optional[str] = None,
        origin_domain: Optional[str] = None,
        signature: Optional[str] = None,
    ) -> None:
        super().__init__(signature)
        if message is not None and len(message) > 300:
            raise ValueError("Message must not exceed 300 characters.")

        self.asset_code = None
        self.asset_issuer = None
        self._asset = asset
        if asset:
            self.asset_code = asset.code
            self.asset_issuer = asset.issuer

        self.memo = None
        self.memo_type = None
        self._memo = memo
        self.memo_type, self.memo = self._encode_memo(memo)
        self.destination = destination
        if isinstance(amount, Decimal):
            amount = str(amount)
        self.amount = amount
        self.callback = callback
        self.msg = message
        self.network_passphrase = network_passphrase
        self.origin_domain = origin_domain

    @staticmethod
    def _encode_memo(memo) -> Union[Tuple[str, Union[str, int]], Tuple[None, None]]:
        if memo and not isinstance(memo, NoneMemo):
            if isinstance(memo, TextMemo):
                memo_text = memo.memo_text.decode()  # memo text cant decode?
                memo_type = "MEMO_TEXT"
                return memo_type, memo_text
            elif isinstance(memo, IdMemo):
                memo_id = memo.memo_id
                memo_type = "MEMO_ID"
                return memo_type, memo_id
            elif isinstance(memo, HashMemo):
                memo_hash = base64.b64encode(memo.memo_hash).decode()
                memo_type = "MEMO_HASH"
                return memo_type, memo_hash
            elif isinstance(memo, ReturnHashMemo):
                memo_return = base64.b64encode(memo.memo_return).decode()
                memo_type = "MEMO_RETURN"
                return memo_type, memo_return
            else:
                raise ValueError("Invalid memo.")
        return None, None

    @staticmethod
    def _decode_memo(
        memo_type: Optional[str], memo_value: Optional[str]
    ) -> Optional[Memo]:
        if memo_type is None:
            return None
        if memo_value is None:
            raise ValueError("`memo` is missing from uri.")
        if memo_type == "MEMO_TEXT":
            return TextMemo(memo_value)
        elif memo_type == "MEMO_ID":
            return IdMemo(int(memo_value))
        elif memo_type == "MEMO_HASH":
            value = base64.b64decode(memo_value.encode())
            return HashMemo(value)
        elif memo_type == "MEMO_RETURN":
            value = base64.b64decode(memo_value.encode())
            return ReturnHashMemo(value)
        else:
            raise ValueError("Invalid `memo_type`.")

    def to_uri(self) -> str:
        """Generate the request URI.

        :return: Stellar Pay URI.
        """
        query_params: Dict[str, Union[str, int, None]] = {}
        query_params["destination"] = self.destination
        if self.amount is not None:
            query_params["amount"] = self.amount
        if self.amount is not None:
            query_params["amount"] = self.amount
        if self._asset is not None and not self._asset.is_native():
            query_params["asset_code"] = self.asset_code
            query_params["asset_issuer"] = self.asset_issuer
        if self._memo is not None and not isinstance(self._memo, NoneMemo):
            assert self.memo is not None
            query_params["memo"] = self.memo
            query_params["memo_type"] = self.memo_type
        if self.callback is not None:
            query_params["callback"] = "url:" + self.callback
        if self.msg is not None:
            query_params["msg"] = self.msg
        if self.network_passphrase is not None:
            query_params["network_passphrase"] = self.network_passphrase
        if self.origin_domain is not None:
            query_params["origin_domain"] = self.origin_domain
        if self.signature is not None:
            query_params["signature"] = self.signature
        # https://github.com/python/typeshed/issues/4234
        return f"{STELLAR_SCHEME}:pay?{parse.urlencode(query_params, quote_via=parse.quote)}"  # type: ignore[type-var]

    @classmethod
    def from_uri(cls, uri: str) -> "PayStellarUri":
        """Parse Stellar Pay URI and generate :class:`PayStellarUri` object.

        :param uri: Stellar Pay URI.
        :return: :class:`PayStellarUri` object from uri.
        """
        parsed_uri = parse.urlparse(uri)
        if parsed_uri.scheme != STELLAR_SCHEME:
            raise ValueError(
                f"Stellar URI scheme should be `{STELLAR_SCHEME}`, but got `{parsed_uri.scheme}`."
            )
        if parsed_uri.path != "pay":
            raise ValueError(
                f"Stellar URI path should be `pay`, but got `{parsed_uri.path}`."
            )
        query = cls._parse_uri_query(parsed_uri.query)
        destination = query.get("destination")
        amount = query.get("amount")
        asset_code = query.get("asset_code")
        asset_issuer = query.get("asset_issuer")
        memo_value = query.get("memo")
        memo_type = query.get("memo_type")
        callback = cls._parse_callback(query.get("callback"))
        msg = query.get("msg")
        network_passphrase = query.get("network_passphrase")
        origin_domain = query.get("origin_domain")
        signature = query.get("signature")
        asset = None
        if asset_code is not None:
            asset = Asset(asset_code, asset_issuer)
        memo = cls._decode_memo(memo_type=memo_type, memo_value=memo_value)

        if destination is None:
            raise ValueError("`destination` is missing from uri.")

        return cls(
            destination=destination,
            amount=amount,
            asset=asset,
            memo=memo,
            callback=callback,
            message=msg,
            network_passphrase=network_passphrase,
            origin_domain=origin_domain,
            signature=signature,
        )

    def __repr__(self):
        return (
            f"<PayStellarUri [destination={self.destination}, amount={self.amount}, "
            f"asset_code={self.asset_code}, asset_issuer={self.asset_issuer}, "
            f"memo={self.memo}, memo_type={self.memo_type}, callback={self.callback}, "
            f"msg={self.msg}, network_passphrase={self.network_passphrase}, "
            f"origin_domain={self.origin_domain}, signature={self.signature}]>"
        )

    def __hash__(self):
        return hash(
            (
                self.destination,
                self.amount,
                self.asset_code,
                self.asset_issuer,
                self.memo,
                self.memo_type,
                self.callback,
                self.msg,
                self.network_passphrase,
                self.origin_domain,
                self.signature,
            )
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.destination == other.destination
            and self.amount == other.amount
            and self.asset_code == other.asset_code
            and self.asset_issuer == other.asset_issuer
            and self.memo == other.memo
            and self.memo_type == other.memo_type
            and self.callback == other.callback
            and self.msg == other.msg
            and self.network_passphrase == other.network_passphrase
            and self.origin_domain == other.origin_domain
            and self.signature == other.signature
        )


class Replacement:
    """Used to represent a single replacement.

    An example::

        r1 = Replacement("sourceAccount", "X", "account on which to create the trustline")
        r2 = Replacement("seqNum", "Y", "sequence for sourceAccount")
        replacements = [r1, r2]

    See `SEP-0007 <https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0007.md#operation-tx>`__

    :param txrep_tx_field_name: Txrep tx field name.
    :param reference_identifier: Reference identifier.
    :param hint: A brief and clear explanation of the context for the `reference_identifier`.

    """

    def __init__(
        self, txrep_tx_field_name: str, reference_identifier: str, hint: str
    ) -> None:
        self.txrep_tx_field_name = txrep_tx_field_name
        self.reference_identifier = reference_identifier
        self.hint = hint

    def __repr__(self):
        return (
            f"<Replacement [txrep_tx_field_name={self.txrep_tx_field_name}, "
            f"reference_identifier={self.reference_identifier}, "
            f"hint={self.hint}]>"
        )

    def __hash__(self):
        return hash((self.txrep_tx_field_name, self.reference_identifier, self.hint))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.txrep_tx_field_name == other.txrep_tx_field_name
            and self.reference_identifier == other.reference_identifier
            and self.hint == other.hint
        )


class TransactionStellarUri(StellarUri):
    """A request for a transaction to be signed.

    See `SEP-0007 <https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0007.md#operation-tx>`__

    :param transaction_envelope: Transaction waiting to be signed.
    :param replace: A value that identifies the fields to be replaced in the xdr using the Txrep (SEP-0011) representation.
    :param callback: The uri to post the transaction to after signing.
    :param pubkey: Specify which public key you want the URI handler to sign for.
    :param message: An message for displaying to the user.
    :param network_passphrase: The passphrase of the target network.
    :param origin_domain: A fully qualified domain name that specifies the originating domain of the URI request.
    :param signature: A base64 encode signature of the hash of the URI request.
    """

    def __init__(
        self,
        transaction_envelope: Union[TransactionEnvelope, FeeBumpTransactionEnvelope],
        replace: Optional[List[Replacement]] = None,
        callback: Optional[str] = None,
        pubkey: Optional[str] = None,
        message: Optional[str] = None,
        network_passphrase: Optional[str] = None,
        origin_domain: Optional[str] = None,
        signature: Optional[str] = None,
    ) -> None:
        super().__init__(signature)
        if message is not None and len(message) > 300:
            raise ValueError("Message must not exceed 300 characters.")

        self.transaction_envelope = transaction_envelope
        self.replace = replace
        self.callback = callback
        self.pubkey = pubkey
        self.msg = message
        self.network_passphrase = network_passphrase
        self.origin_domain = origin_domain

    @property
    def _replace(self) -> Optional[str]:
        if not self.replace:
            return None
        replaces = []
        hits = dict()
        for i in self.replace:
            hits[i.reference_identifier] = i.hint
            replaces.append(i.txrep_tx_field_name + ":" + i.reference_identifier)
        return (
            ",".join(replaces) + ";" + ",".join([k + ":" + v for k, v in hits.items()])
        )

    def to_uri(self) -> str:
        """Generate the request URI.

        :return: Stellar Transaction URI.
        """
        query_params = dict()
        query_params["xdr"] = self.transaction_envelope.to_xdr()
        if self.callback is not None:
            query_params["callback"] = "url:" + self.callback
        replace = self._replace
        if replace is not None:
            query_params["replace"] = replace
        if self.pubkey is not None:
            query_params["pubkey"] = self.pubkey
        if self.msg is not None:
            query_params["msg"] = self.msg
        if self.network_passphrase is not None:
            query_params["network_passphrase"] = self.network_passphrase
        if self.origin_domain is not None:
            query_params["origin_domain"] = self.origin_domain
        if self.signature is not None:
            query_params["signature"] = self.signature
        return f"{STELLAR_SCHEME}:tx?{parse.urlencode(query_params, quote_via=parse.quote)}"  # type: ignore[type-var]

    @classmethod
    def from_uri(
        cls, uri: str, network_passphrase: Optional[str]
    ) -> "TransactionStellarUri":
        """Parse Stellar Transaction URI and generate :class:`TransactionStellarUri` object.

        :param uri: Stellar Transaction URI.
        :param network_passphrase: The network to connect to for verifying and retrieving xdr,
            If it is set to `None`, the `network_passphrase` in the uri will not be verified.
        :return: :class:`TransactionStellarUri` object from uri.
        """
        parsed_uri = parse.urlparse(uri)
        if parsed_uri.scheme != STELLAR_SCHEME:
            raise ValueError(
                f"Stellar URI scheme should be `{STELLAR_SCHEME}`, but got `{parsed_uri.scheme}`."
            )
        if parsed_uri.path != "tx":
            raise ValueError(
                f"Stellar URI path should be `tx`, but got `{parsed_uri.path}`."
            )
        query = cls._parse_uri_query(parsed_uri.query)
        uri_network_passphrase = query.get("network_passphrase")
        if network_passphrase is None and uri_network_passphrase is None:
            raise ValueError("`network_passphrase` is required.")

        if (
            uri_network_passphrase is not None
            and network_passphrase is not None
            and network_passphrase != uri_network_passphrase
        ):
            raise ValueError(
                "The `network_passphrase` in the function parameter does not "
                "match the `network_passphrase` in the uri."
            )
        network_passphrase = network_passphrase or uri_network_passphrase
        assert network_passphrase is not None

        xdr = query.get("xdr")
        callback = cls._parse_callback(query.get("callback"))
        pubkey = query.get("pubkey")
        msg = query.get("msg")
        origin_domain = query.get("origin_domain")
        signature = query.get("signature")
        if xdr is None:
            raise ValueError("`xdr` is missing from uri.")
        if FeeBumpTransactionEnvelope.is_fee_bump_transaction_envelope(xdr):
            tx = FeeBumpTransactionEnvelope.from_xdr(xdr, network_passphrase)
        else:
            tx = TransactionEnvelope.from_xdr(xdr, network_passphrase)  # type: ignore[assignment]
        raw_replacements = query.get("replace")
        replacements = []
        if raw_replacements is not None:
            descriptions_map = {}
            identifiers, descriptions = raw_replacements.split(";")
            for description in descriptions.split(","):
                k, v = description.split(":")
                descriptions_map[k] = v
            for identifier in identifiers.split(","):
                k, v = identifier.split(":")
                hint = descriptions_map.get(v)
                if hint is None:
                    raise ValueError("Invalid `replace`.")
                replacement = Replacement(k, v, hint)
                replacements.append(replacement)
        return cls(
            transaction_envelope=tx,
            replace=replacements,
            callback=callback,
            pubkey=pubkey,
            message=msg,
            network_passphrase=network_passphrase,
            origin_domain=origin_domain,
            signature=signature,
        )

    def __repr__(self):
        return (
            f"<TransactionStellarUri [xdr={self.transaction_envelope.to_xdr()}, replace={self.replace}, "
            f"callback={self.callback}, pubkey={self.pubkey}, "
            f"msg={self.msg}, network_passphrase={self.network_passphrase}, "
            f"origin_domain={self.origin_domain}, signature={self.signature}]>"
        )

    def __hash__(self):
        return hash(
            (
                self.transaction_envelope,
                self.replace,
                self.callback,
                self.pubkey,
                self.msg,
                self.network_passphrase,
                self.origin_domain,
                self.signature,
            )
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.transaction_envelope == other.transaction_envelope
            and self.replace == other.replace
            and self.callback == other.callback
            and self.pubkey == other.pubkey
            and self.msg == other.msg
            and self.network_passphrase == other.network_passphrase
            and self.origin_domain == other.origin_domain
            and self.signature == other.signature
        )
