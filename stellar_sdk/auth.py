import copy
import itertools
import random
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from typing import TypeAlias

from . import scval
from . import xdr as stellar_xdr
from .address import Address, AddressType
from .keypair import Keypair
from .network import Network
from .utils import sha256

AuthorizationSigner: TypeAlias = Callable[
    [stellar_xdr.HashIDPreimage], stellar_xdr.SCVal
]
"""Type alias for a custom Soroban authorization signer.

Receives the authorization preimage and returns the signature ``SCVal`` accepted
by the account contract at the entry's address. Use
:func:`authorization_payload_hash` to obtain the same 32-byte payload that the
account's ``__check_auth`` would receive.
"""

__all__ = [
    "AuthorizationSigner",
    "DelegateSignature",
    "authorization_payload_hash",
    "authorize_entry",
    "authorize_invocation",
    "build_authorization_preimage",
    "build_with_delegates_entry",
]


def authorization_payload_hash(preimage: stellar_xdr.HashIDPreimage) -> bytes:
    """Return the 32-byte payload that account contracts receive in ``__check_auth``.

    Use this inside a custom :data:`AuthorizationSigner` to obtain the bytes the
    host hashes from the authorization preimage and asks the account contract
    to verify.

    :param preimage: The Soroban authorization preimage.
    :return: SHA-256 hash of the preimage XDR bytes.
    """
    return sha256(preimage.to_xdr_bytes())


def _get_address_credentials(
    credentials: stellar_xdr.SorobanCredentials,
) -> stellar_xdr.SorobanAddressCredentials | None:
    """Extract the address credentials from any address-based credential type.

    Returns the inner :class:`stellar_sdk.xdr.SorobanAddressCredentials`
    reference (assigning to its fields writes back into the entry), or ``None``
    for source-account credentials, which carry no address payload.
    """
    if (
        credentials.type
        == stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS
    ):
        assert credentials.address is not None
        return credentials.address
    if (
        credentials.type
        == stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_V2
    ):
        assert credentials.address_v2 is not None
        return credentials.address_v2
    if (
        credentials.type
        == stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_WITH_DELEGATES
    ):
        assert credentials.address_with_delegates is not None
        return credentials.address_with_delegates.address_credentials
    return None


def _collect_signature_nodes(
    credentials: stellar_xdr.SorobanCredentials,
) -> list[stellar_xdr.SorobanAddressCredentials | stellar_xdr.SorobanDelegateSignature]:
    """Every node in ``credentials`` that can carry a signature, in a stable
    order: the top-level address credentials first, then (only for
    ``SOROBAN_CREDENTIALS_ADDRESS_WITH_DELEGATES``) the delegates and their
    nested delegates, depth-first. Per CAP-71-01 all of these nodes commit to
    the same payload — the one bound to the top-level address.
    """
    addr_auth = _get_address_credentials(credentials)
    if addr_auth is None:
        return []
    nodes: list[
        stellar_xdr.SorobanAddressCredentials | stellar_xdr.SorobanDelegateSignature
    ] = [addr_auth]
    if (
        credentials.type
        == stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_WITH_DELEGATES
    ):
        assert credentials.address_with_delegates is not None

        def walk(delegates: list[stellar_xdr.SorobanDelegateSignature]) -> None:
            for delegate in delegates:
                nodes.append(delegate)
                walk(delegate.nested_delegates)

        walk(credentials.address_with_delegates.delegates)
    return nodes


def build_authorization_preimage(
    entry: stellar_xdr.SorobanAuthorizationEntry,
    valid_until_ledger_sequence: int,
    network_passphrase: str,
) -> stellar_xdr.HashIDPreimage:
    """Build the signature preimage for a Soroban address authorization entry.

    For ``SOROBAN_CREDENTIALS_ADDRESS`` this is the legacy, non-address-bound
    ``ENVELOPE_TYPE_SOROBAN_AUTHORIZATION`` preimage. For
    ``SOROBAN_CREDENTIALS_ADDRESS_V2`` and
    ``SOROBAN_CREDENTIALS_ADDRESS_WITH_DELEGATES`` it is the address-bound
    ``ENVELOPE_TYPE_SOROBAN_AUTHORIZATION_WITH_ADDRESS`` preimage (CAP-71). For
    the delegates variant this single payload — bound to the *top-level*
    address — is what the top-level account and every (nested) delegate each
    sign.

    :param entry: Soroban authorization entry to be authorized.
    :param valid_until_ledger_sequence: Ledger sequence through which this
        authorization entry should remain valid.
    :param network_passphrase: Network passphrase incorporated into the signature.
    :return: A :class:`stellar_sdk.xdr.HashIDPreimage` for the authorization.
    :raises:
        :exc:`ValueError`: if ``entry`` does not use address credentials, or if
        the credential address is not a classic account (``G...``) or contract
        (``C...``) address.
    """
    addr_auth = _get_address_credentials(entry.credentials)
    if addr_auth is None:
        raise ValueError("Only address credentials can be authorized.")
    _ensure_authorization_sc_address(addr_auth.address)
    network_id = Network(network_passphrase).network_id()
    if (
        entry.credentials.type
        == stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS
    ):
        return stellar_xdr.HashIDPreimage(
            type=stellar_xdr.EnvelopeType.ENVELOPE_TYPE_SOROBAN_AUTHORIZATION,
            soroban_authorization=stellar_xdr.HashIDPreimageSorobanAuthorization(
                network_id=stellar_xdr.Hash(network_id),
                nonce=addr_auth.nonce,
                signature_expiration_ledger=stellar_xdr.Uint32(
                    valid_until_ledger_sequence
                ),
                invocation=entry.root_invocation,
            ),
        )
    # ADDRESS_V2 and ADDRESS_WITH_DELEGATES bind the address into the signed
    # payload (CAP-71); for the delegates variant it is the top-level address.
    return stellar_xdr.HashIDPreimage(
        type=stellar_xdr.EnvelopeType.ENVELOPE_TYPE_SOROBAN_AUTHORIZATION_WITH_ADDRESS,
        soroban_authorization_with_address=stellar_xdr.HashIDPreimageSorobanAuthorizationWithAddress(
            network_id=stellar_xdr.Hash(network_id),
            nonce=addr_auth.nonce,
            signature_expiration_ledger=stellar_xdr.Uint32(valid_until_ledger_sequence),
            address=addr_auth.address,
            invocation=entry.root_invocation,
        ),
    )


def _default_account_signature_scval(
    public_key: bytes, signature: bytes
) -> stellar_xdr.SCVal:
    """Build the signature ``SCVal`` shape expected by the default Stellar Account contract.

    Shape: ``Vec<Map{public_key: Bytes, signature: Bytes}>``. Documented at
    https://developers.stellar.org/docs/learn/fundamentals/contract-development/contract-interactions/stellar-transaction#stellar-account-signatures
    """
    return scval.to_vec(
        [
            scval.to_map(
                {
                    scval.to_symbol("public_key"): scval.to_bytes(public_key),
                    scval.to_symbol("signature"): scval.to_bytes(signature),
                }
            )
        ]
    )


def _sign_authorization(
    signer: Keypair | AuthorizationSigner,
    preimage: stellar_xdr.HashIDPreimage,
) -> stellar_xdr.SCVal:
    if isinstance(signer, Keypair):
        payload = authorization_payload_hash(preimage)
        return _default_account_signature_scval(
            signer.raw_public_key(), signer.sign(payload)
        )
    result = signer(preimage)
    if not isinstance(result, stellar_xdr.SCVal):
        raise TypeError(
            "Authorization signer must return a stellar_sdk.xdr.SCVal "
            "(the legacy (public_key, signature) tuple form is no longer supported)."
        )
    return result


_AUTHORIZED_ADDRESS_TYPES = (AddressType.ACCOUNT, AddressType.CONTRACT)
_AUTHORIZED_SC_ADDRESS_TYPES = (
    stellar_xdr.SCAddressType.SC_ADDRESS_TYPE_ACCOUNT,
    stellar_xdr.SCAddressType.SC_ADDRESS_TYPE_CONTRACT,
)
_AUTHORIZED_ADDRESS_ERROR = (
    "Authorization address must be a classic account (G...) or contract (C...) address."
)


def _ensure_authorization_sc_address(address: stellar_xdr.SCAddress) -> None:
    if address.type not in _AUTHORIZED_SC_ADDRESS_TYPES:
        raise ValueError(_AUTHORIZED_ADDRESS_ERROR)


def _resolve_account_or_contract_address(address: Address | str) -> Address:
    resolved = address if isinstance(address, Address) else Address(address)
    if resolved.type not in _AUTHORIZED_ADDRESS_TYPES:
        raise ValueError(_AUTHORIZED_ADDRESS_ERROR)
    return resolved


def _resolve_address(address: Address | str) -> stellar_xdr.SCAddress:
    return _resolve_account_or_contract_address(address).to_xdr_sc_address()


def authorize_entry(
    entry: stellar_xdr.SorobanAuthorizationEntry | str,
    signer: Keypair | AuthorizationSigner,
    valid_until_ledger_sequence: int,
    network_passphrase: str,
    *,
    for_address: Address | str | None = None,
) -> stellar_xdr.SorobanAuthorizationEntry:
    """Sign an existing Soroban authorization entry, returning a signed copy.

    "Fills out" the authorization with the credentials, expiration ledger, and
    a signature shaped for the account at the entry's address — be it the
    default Stellar Account (when ``signer`` is a :class:`Keypair`) or any
    custom account contract (when ``signer`` is an :data:`AuthorizationSigner`
    callable that returns the contract-defined signature ``SCVal``).

    Supports ``SOROBAN_CREDENTIALS_ADDRESS``, ``SOROBAN_CREDENTIALS_ADDRESS_V2``,
    and ``SOROBAN_CREDENTIALS_ADDRESS_WITH_DELEGATES`` (CAP-71, Protocol 27+)
    credentials. Source-account credentials are returned unchanged.

    The signed payload commits to ``valid_until_ledger_sequence``, and for a
    delegates entry the top-level account and every (nested) delegate sign the
    same payload — so every signer of one entry must use the same
    ``valid_until_ledger_sequence``, otherwise earlier signatures are
    invalidated.

    Default account example::

        signed = authorize_entry(entry, keypair, valid_until, passphrase)

    Custom account example (BLS, WebAuthn, threshold, ...)::

        from stellar_sdk import scval, xdr
        from stellar_sdk.auth import authorization_payload_hash, authorize_entry

        def bls_signer(preimage: xdr.HashIDPreimage) -> xdr.SCVal:
            payload = authorization_payload_hash(preimage)
            return scval.to_bytes(my_bls_sign(payload))  # whatever shape the contract expects

        signed = authorize_entry(entry, bls_signer, valid_until, passphrase)

    :param entry: Unsigned Soroban authorization entry, either a
        :class:`stellar_xdr.SorobanAuthorizationEntry` or its base64 XDR string.
    :param signer: Either a :class:`Keypair` (uses the default Stellar Account
        signature shape) or an :data:`AuthorizationSigner` callable. The signer
        must produce a signature accepted by the account at the credential node
        being signed.
    :param valid_until_ledger_sequence: Ledger sequence through which this
        authorization entry should remain valid (the entry is invalid starting
        at ``validUntil + 1``).
    :param network_passphrase: Network passphrase incorporated into the signature
        (see :class:`stellar_sdk.Network` for options).
    :param for_address: Which credential node the signature should be written
        to (CAP-71-01). When omitted, the signature is written to the top-level
        credentials — the behavior for ``ADDRESS`` / ``ADDRESS_V2`` entries and
        for accounts whose signing key differs from the credential address
        (e.g. multisig). When given, the signature is written to every credential
        node (top-level or delegate, possibly nested) whose address matches.
    :return: A signed Soroban authorization entry.
    :raises:
        :exc:`ValueError`: if the entry's credential address is not a classic
        account (``G...``) or contract (``C...``) address, or if ``for_address``
        matches no credential node in the entry.
    """
    if isinstance(entry, str):
        entry = stellar_xdr.SorobanAuthorizationEntry.from_xdr(entry)
    else:
        entry = copy.deepcopy(entry)

    if (
        entry.credentials.type
        == stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_SOURCE_ACCOUNT
    ):
        return entry

    addr_auth = _get_address_credentials(entry.credentials)
    if addr_auth is None:
        raise ValueError(
            f"Unsupported SorobanCredentialsType: {entry.credentials.type}."
        )

    # Set the expiration before building the preimage, so the signed payload
    # commits to the same expiration ledger stored in the credentials.
    addr_auth.signature_expiration_ledger = stellar_xdr.Uint32(
        valid_until_ledger_sequence
    )

    preimage = build_authorization_preimage(
        entry, valid_until_ledger_sequence, network_passphrase
    )
    signature = _sign_authorization(signer, preimage)

    # CAP-71-01: the payload is shared across the top-level address and every
    # (possibly nested) delegate, so the signature can be written to whichever
    # credential node(s) carry `for_address`.
    if for_address is None:
        targets: list[
            stellar_xdr.SorobanAddressCredentials | stellar_xdr.SorobanDelegateSignature
        ] = [addr_auth]
    else:
        resolved = _resolve_account_or_contract_address(for_address)
        targets = [
            node
            for node in _collect_signature_nodes(entry.credentials)
            if Address.from_xdr_sc_address(node.address).address == resolved.address
        ]
        if not targets:
            raise ValueError(
                "The authorization entry has no credential node for address "
                f"{resolved.address}."
            )
    for node in targets:
        node.signature = signature
    return entry


def authorize_invocation(
    signer: Keypair | AuthorizationSigner,
    address: Address | str | None,
    valid_until_ledger_sequence: int,
    invocation: stellar_xdr.SorobanAuthorizedInvocation,
    network_passphrase: str,
    *,
    credentials_type: stellar_xdr.SorobanCredentialsType = stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS,
) -> stellar_xdr.SorobanAuthorizationEntry:
    """Build a fresh Soroban authorization entry from scratch and sign it.

    Expresses authorization as a function of:

    * a particular identity — a signing :class:`Keypair`, an account contract,
      or any other custom signer
    * approving the execution of an invocation tree (typically a
      simulation-acquired :class:`stellar_xdr.SorobanAuthorizedInvocation`)
    * on a particular network (uniquely identified by its passphrase, see
      :class:`stellar_sdk.Network`)
    * until a particular ledger sequence is reached

    This is the "build" counterpart of :func:`authorize_entry`, which signs an
    existing entry "in place".

    By default the entry uses the legacy ``SOROBAN_CREDENTIALS_ADDRESS``
    credentials, which are valid on every network. Pass
    ``credentials_type=SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_V2``
    to opt in to the address-bound credentials (CAP-71-02), which bind the
    signature to ``address`` but require the network to run Protocol 27 or
    later — emitting them before a network upgrades fails submission. This
    default is expected to flip to ``SOROBAN_CREDENTIALS_ADDRESS_V2`` once a
    later protocol makes the address-bound payload mandatory.

    :param signer: Either a :class:`Keypair` or an :data:`AuthorizationSigner`
        callable. See :func:`authorize_entry` for details.
    :param address: The address being authorized. Must be a classic ``G...``
        account address or a ``C...`` contract address, or an
        :class:`Address` instance of one of those types. When ``signer`` is a
        :class:`Keypair`, may be omitted (defaults to the keypair's public key);
        otherwise required.
    :param valid_until_ledger_sequence: Ledger sequence through which this
        authorization entry should remain valid.
    :param invocation: Invocation tree being authorized (typically from
        transaction simulation).
    :param network_passphrase: Network passphrase incorporated into the signature.
    :param credentials_type: The credential type for the new entry, either the
        legacy ``SOROBAN_CREDENTIALS_ADDRESS`` (default) or
        ``SOROBAN_CREDENTIALS_ADDRESS_V2`` (Protocol 27+). To build a
        ``SOROBAN_CREDENTIALS_ADDRESS_WITH_DELEGATES`` entry, use
        :func:`build_with_delegates_entry` instead.
    :return: A signed Soroban authorization entry.
    :raises:
        :exc:`ValueError`: if ``address`` is omitted with a non-Keypair signer,
        if ``address`` is not a classic account (``G...``) or contract
        (``C...``) address, or if ``credentials_type`` is not
        ``SOROBAN_CREDENTIALS_ADDRESS`` / ``SOROBAN_CREDENTIALS_ADDRESS_V2``.
    """
    if address is None:
        if isinstance(signer, Keypair):
            address = signer.public_key
        else:
            raise ValueError("`address` is required when `signer` is not a Keypair.")

    nonce = random.randint(-(2**63), 2**63 - 1)
    address_credentials = stellar_xdr.SorobanAddressCredentials(
        address=_resolve_address(address),
        nonce=stellar_xdr.Int64(nonce),
        signature_expiration_ledger=stellar_xdr.Uint32(0),
        signature=stellar_xdr.SCVal(type=stellar_xdr.SCValType.SCV_VOID),
    )
    if (
        credentials_type
        == stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS
    ):
        credentials = stellar_xdr.SorobanCredentials(
            type=credentials_type, address=address_credentials
        )
    elif (
        credentials_type
        == stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_V2
    ):
        credentials = stellar_xdr.SorobanCredentials(
            type=credentials_type, address_v2=address_credentials
        )
    else:
        raise ValueError(
            "`credentials_type` must be SOROBAN_CREDENTIALS_ADDRESS or "
            "SOROBAN_CREDENTIALS_ADDRESS_V2; use `build_with_delegates_entry` to "
            "build SOROBAN_CREDENTIALS_ADDRESS_WITH_DELEGATES entries."
        )
    entry = stellar_xdr.SorobanAuthorizationEntry(
        root_invocation=invocation,
        credentials=credentials,
    )
    return authorize_entry(
        entry, signer, valid_until_ledger_sequence, network_passphrase
    )


@dataclass
class DelegateSignature:
    """A delegate signer to attach to a
    ``SOROBAN_CREDENTIALS_ADDRESS_WITH_DELEGATES`` entry via
    :func:`build_with_delegates_entry` (CAP-71-01, Protocol 27+).
    """

    address: Address | str
    """The delegate's address (``G...`` account or ``C...`` contract)."""

    signature: stellar_xdr.SCVal | None = None
    """The delegate's signature value. Defaults to an ``scvVoid`` placeholder,
    which can be filled afterwards with :func:`authorize_entry` (passing this
    address as ``for_address``) or by editing the entry directly."""

    nested_delegates: list["DelegateSignature"] = field(default_factory=list)
    """Signers this delegate in turn delegates to (recursive)."""


def _build_delegate_nodes(
    delegates: Sequence[DelegateSignature],
) -> list[stellar_xdr.SorobanDelegateSignature]:
    """Recursively convert :class:`DelegateSignature` descriptors into
    :class:`stellar_sdk.xdr.SorobanDelegateSignature` nodes, sorting each level
    by address and rejecting duplicates (CAP-71-01)."""
    nodes = [
        stellar_xdr.SorobanDelegateSignature(
            address=_resolve_address(delegate.address),
            signature=(
                delegate.signature
                if delegate.signature is not None
                else stellar_xdr.SCVal(type=stellar_xdr.SCValType.SCV_VOID)
            ),
            nested_delegates=_build_delegate_nodes(delegate.nested_delegates),
        )
        for delegate in delegates
    ]
    nodes.sort(key=lambda node: node.address.to_xdr_bytes())
    for previous, current in itertools.pairwise(nodes):
        if previous.address.to_xdr_bytes() == current.address.to_xdr_bytes():
            raise ValueError(
                "Duplicate delegate address: "
                f"{Address.from_xdr_sc_address(current.address).address}."
            )
    return nodes


def build_with_delegates_entry(
    entry: stellar_xdr.SorobanAuthorizationEntry | str,
    valid_until_ledger_sequence: int,
    delegates: Sequence[DelegateSignature],
    signature: stellar_xdr.SCVal | None = None,
) -> stellar_xdr.SorobanAuthorizationEntry:
    """Build a ``SOROBAN_CREDENTIALS_ADDRESS_WITH_DELEGATES`` authorization
    entry by wrapping the address credentials of an existing ``ADDRESS`` /
    ``ADDRESS_V2`` entry (e.g. one returned by simulation) together with a
    caller-provided set of delegate signers (CAP-71-01, Protocol 27+).

    Simulation never emits the delegates variant on its own — which accounts
    use delegated authentication is account-specific policy known only to the
    client (much like a multisig policy). This helper just assembles the
    wrapper XDR; you supply the delegate tree (addresses and, optionally,
    signatures). To produce the signatures, build the shared payload with
    :func:`build_authorization_preimage` on the returned entry and sign it, or
    fill each node afterwards with :func:`authorize_entry`, passing the
    signer's address as ``for_address`` and the same
    ``valid_until_ledger_sequence`` as given here (the shared payload commits
    to it).

    Each delegates array (the top-level set and every ``nested_delegates``) is
    sorted by address in ascending XDR-byte order, and duplicate addresses
    within an array are rejected, as the protocol requires — otherwise the host
    rejects the entry.

    :param entry: An existing ``SOROBAN_CREDENTIALS_ADDRESS`` or
        ``SOROBAN_CREDENTIALS_ADDRESS_V2`` entry whose address credentials
        should be wrapped, either a
        :class:`stellar_xdr.SorobanAuthorizationEntry` or its base64 XDR string.
    :param valid_until_ledger_sequence: The expiration ledger sequence stored on
        the top-level credentials.
    :param delegates: The delegate signers to attach.
    :param signature: The top-level account's signature. Defaults to
        ``scvVoid``, which is valid for accounts that authorize purely via
        delegated signers.
    :return: A new ``SOROBAN_CREDENTIALS_ADDRESS_WITH_DELEGATES`` authorization
        entry; the input entry is not modified.
    :raises:
        :exc:`ValueError`: if ``entry`` does not carry ``ADDRESS`` /
        ``ADDRESS_V2`` credentials, if any delegates array contains a duplicate
        address, or if any delegate address is not a classic account (``G...``)
        or contract (``C...``) address.
    """
    if isinstance(entry, str):
        entry = stellar_xdr.SorobanAuthorizationEntry.from_xdr(entry)
    else:
        entry = copy.deepcopy(entry)

    if entry.credentials.type not in (
        stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS,
        stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_V2,
    ):
        raise ValueError(
            "`entry` must use SOROBAN_CREDENTIALS_ADDRESS or "
            f"SOROBAN_CREDENTIALS_ADDRESS_V2 credentials, got {entry.credentials.type}."
        )
    addr_auth = _get_address_credentials(entry.credentials)
    assert addr_auth is not None

    return stellar_xdr.SorobanAuthorizationEntry(
        credentials=stellar_xdr.SorobanCredentials(
            type=stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_WITH_DELEGATES,
            address_with_delegates=stellar_xdr.SorobanAddressCredentialsWithDelegates(
                address_credentials=stellar_xdr.SorobanAddressCredentials(
                    address=addr_auth.address,
                    nonce=addr_auth.nonce,
                    signature_expiration_ledger=stellar_xdr.Uint32(
                        valid_until_ledger_sequence
                    ),
                    signature=(
                        signature
                        if signature is not None
                        else stellar_xdr.SCVal(type=stellar_xdr.SCValType.SCV_VOID)
                    ),
                ),
                delegates=_build_delegate_nodes(delegates),
            ),
        ),
        root_invocation=entry.root_invocation,
    )
