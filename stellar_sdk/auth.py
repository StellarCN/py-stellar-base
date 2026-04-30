import copy
import random
from typing import Callable

from . import scval
from . import xdr as stellar_xdr
from .address import Address
from .keypair import Keypair
from .network import Network
from .utils import sha256

AuthorizationSigner = Callable[[stellar_xdr.HashIDPreimage], stellar_xdr.SCVal]
"""Type alias for a custom Soroban authorization signer.

Receives the authorization preimage and returns the signature ``SCVal`` accepted
by the account contract at the entry's address. Use
:func:`authorization_payload_hash` to obtain the same 32-byte payload that the
account's ``__check_auth`` would receive.
"""

__all__ = [
    "AuthorizationSigner",
    "authorization_payload_hash",
    "authorize_entry",
    "authorize_invocation",
    "build_authorization_preimage",
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


def build_authorization_preimage(
    entry: stellar_xdr.SorobanAuthorizationEntry,
    valid_until_ledger_sequence: int,
    network_passphrase: str,
) -> stellar_xdr.HashIDPreimage:
    """Build the signature preimage for a Soroban address authorization entry.

    :param entry: Soroban authorization entry to be authorized.
    :param valid_until_ledger_sequence: Exclusive future ledger sequence number
        until which this authorization entry should be valid.
    :param network_passphrase: Network passphrase incorporated into the signature.
    :return: A :class:`stellar_sdk.xdr.HashIDPreimage` for the authorization.
    :raises:
        :exc:`ValueError`: if ``entry`` does not use address credentials.
    """
    if (
        entry.credentials.type
        != stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS
    ):
        raise ValueError("Only address credentials can be authorized.")

    assert entry.credentials.address is not None
    addr_auth = entry.credentials.address
    network_id = Network(network_passphrase).network_id()
    return stellar_xdr.HashIDPreimage(
        type=stellar_xdr.EnvelopeType.ENVELOPE_TYPE_SOROBAN_AUTHORIZATION,
        soroban_authorization=stellar_xdr.HashIDPreimageSorobanAuthorization(
            network_id=stellar_xdr.Hash(network_id),
            nonce=addr_auth.nonce,
            signature_expiration_ledger=stellar_xdr.Uint32(valid_until_ledger_sequence),
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


def _resolve_address(address: Address | str) -> stellar_xdr.SCAddress:
    return (
        address if isinstance(address, Address) else Address(address)
    ).to_xdr_sc_address()


def authorize_entry(
    entry: stellar_xdr.SorobanAuthorizationEntry | str,
    signer: Keypair | AuthorizationSigner,
    valid_until_ledger_sequence: int,
    network_passphrase: str,
) -> stellar_xdr.SorobanAuthorizationEntry:
    """Sign an existing Soroban authorization entry, returning a signed copy.

    "Fills out" the authorization with the credentials, expiration ledger, and
    a signature shaped for the account at the entry's address — be it the
    default Stellar Account (when ``signer`` is a :class:`Keypair`) or any
    custom account contract (when ``signer`` is an :data:`AuthorizationSigner`
    callable that returns the contract-defined signature ``SCVal``).

    Source-account credentials are returned unchanged.

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
        must produce a signature accepted by the account at
        ``entry.credentials.address``.
    :param valid_until_ledger_sequence: Exclusive future ledger sequence number
        until which this authorization entry should be valid (when
        ``currentLedgerSeq == validUntil``, the entry is expired).
    :param network_passphrase: Network passphrase incorporated into the signature
        (see :class:`stellar_sdk.Network` for options).
    :return: A signed Soroban authorization entry.
    """
    if isinstance(entry, str):
        entry = stellar_xdr.SorobanAuthorizationEntry.from_xdr(entry)
    else:
        entry = copy.deepcopy(entry)

    if (
        entry.credentials.type
        != stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS
    ):
        return entry

    assert entry.credentials.address is not None
    addr_auth = entry.credentials.address
    addr_auth.signature_expiration_ledger = stellar_xdr.Uint32(
        valid_until_ledger_sequence
    )

    preimage = build_authorization_preimage(
        entry, valid_until_ledger_sequence, network_passphrase
    )
    addr_auth.signature = _sign_authorization(signer, preimage)
    return entry


def authorize_invocation(
    signer: Keypair | AuthorizationSigner,
    address: Address | str | None,
    valid_until_ledger_sequence: int,
    invocation: stellar_xdr.SorobanAuthorizedInvocation,
    network_passphrase: str,
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

    :param signer: Either a :class:`Keypair` or an :data:`AuthorizationSigner`
        callable. See :func:`authorize_entry` for details.
    :param address: The address being authorized. May be a classic ``G...``
        account address or a ``C...`` contract address. When ``signer`` is a
        :class:`Keypair`, may be omitted (defaults to the keypair's public key);
        otherwise required.
    :param valid_until_ledger_sequence: Exclusive future ledger sequence number
        until which this authorization entry should be valid.
    :param invocation: Invocation tree being authorized (typically from
        transaction simulation).
    :param network_passphrase: Network passphrase incorporated into the signature.
    :return: A signed Soroban authorization entry.
    :raises:
        :exc:`ValueError`: if ``address`` is omitted with a non-Keypair signer.
    """
    if address is None:
        if isinstance(signer, Keypair):
            address = signer.public_key
        else:
            raise ValueError("`address` is required when `signer` is not a Keypair.")

    nonce = random.randint(-(2**63), 2**63 - 1)
    entry = stellar_xdr.SorobanAuthorizationEntry(
        root_invocation=invocation,
        credentials=stellar_xdr.SorobanCredentials(
            type=stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS,
            address=stellar_xdr.SorobanAddressCredentials(
                address=_resolve_address(address),
                nonce=stellar_xdr.Int64(nonce),
                signature_expiration_ledger=stellar_xdr.Uint32(0),
                signature=stellar_xdr.SCVal(type=stellar_xdr.SCValType.SCV_VOID),
            ),
        ),
    )
    return authorize_entry(
        entry, signer, valid_until_ledger_sequence, network_passphrase
    )
