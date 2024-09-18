import copy
import random
from typing import Callable, Optional, Union

from . import scval
from . import xdr as stellar_xdr
from .address import Address
from .exceptions import BadSignatureError
from .keypair import Keypair
from .network import Network
from .utils import sha256

__all__ = ["authorize_entry", "authorize_invocation"]


def authorize_entry(
    entry: Union[stellar_xdr.SorobanAuthorizationEntry, str],
    signer: Union[Keypair, Callable[[stellar_xdr.HashIDPreimage], bytes]],
    valid_until_ledger_sequence: int,
    network_passphrase: str,
) -> stellar_xdr.SorobanAuthorizationEntry:
    """Actually authorizes an existing authorization entry using the given the
    credentials and expiration details, returning a signed copy.

    This "fills out" the authorization entry with a signature, indicating to the
    :class:`stellar_sdk.InvokeHostFunction` it's attached to that:

    * a particular identity (i.e. signing :class:`stellar_sdk.Keypair` or other signer)
    * approving the execution of an invocation tree (i.e. a
        simulation-acquired :class:`stellar_xdr.SorobanAuthorizedInvocation` or otherwise built)
    * on a particular network (uniquely identified by its passphrase, see :class:`stellar_sdk.Network`)
    * until a particular ledger sequence is reached.

    Note that if using the function form of `signer`, the signer is assumed to be
    the entry's credential address. If you need a different key to sign the
    entry, you will need to use different method (e.g., fork this code).

    :param entry: an unsigned Soroban authorization entry.
    :param signer: either a :class:`Keypair` or a function which takes a payload
        (a :class:`stellar_xdr.HashIDPreimage` instance) input and returns a bytes signature,
        the signing key should correspond to the address in the `entry`.
    :param valid_until_ledger_sequence: the (exclusive) future ledger sequence number until which
        this authorization entry should be valid (if `currentLedgerSeq==validUntil`, this is expired)
    :param network_passphrase: the network passphrase is incorporated into the signature (see :class:`stellar_sdk.Network` for options)
    :return: a signed Soroban authorization entry.
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

    network_id = Network(network_passphrase).network_id()
    preimage = stellar_xdr.HashIDPreimage(
        type=stellar_xdr.EnvelopeType.ENVELOPE_TYPE_SOROBAN_AUTHORIZATION,
        soroban_authorization=stellar_xdr.HashIDPreimageSorobanAuthorization(
            network_id=stellar_xdr.Hash(network_id),
            nonce=addr_auth.nonce,
            signature_expiration_ledger=addr_auth.signature_expiration_ledger,
            invocation=entry.root_invocation,
        ),
    )
    payload = sha256(preimage.to_xdr_bytes())
    if isinstance(signer, Keypair):
        signature = signer.sign(payload)
        public_key = signer.raw_public_key()
    else:
        signature = signer(preimage)
        public_key = Address.from_xdr_sc_address(addr_auth.address).key

    try:
        Keypair.from_raw_ed25519_public_key(public_key).verify(payload, signature)
    except BadSignatureError as e:
        raise ValueError("signature doesn't match payload.") from e

    # This structure is defined here:
    # https://soroban.stellar.org/docs/fundamentals-and-concepts/invoking-contracts-with-transactions#stellar-account-signatures
    addr_auth.signature = scval.to_vec(
        [
            scval.to_map(
                {
                    scval.to_symbol("public_key"): scval.to_bytes(public_key),
                    scval.to_symbol("signature"): scval.to_bytes(signature),
                }
            )
        ]
    )
    return entry


def authorize_invocation(
    signer: Union[Keypair, Callable[[stellar_xdr.HashIDPreimage], bytes]],
    public_key: Optional[str],
    valid_until_ledger_sequence: int,
    invocation: stellar_xdr.SorobanAuthorizedInvocation,
    network_passphrase: str,
):
    """This builds an entry from scratch, allowing you to express authorization as a function of:

    * a particular identity (i.e. signing :class:`stellar_sdk.Keypair` or other signer)
    * approving the execution of an invocation tree (i.e. a
        simulation-acquired :class:`stellar_xdr.SorobanAuthorizedInvocation` or otherwise built)
    * on a particular network (uniquely identified by its passphrase, see :class:`stellar_sdk.Network`)
    * until a particular ledger sequence is reached.

    This is in contrast to :func:`authorize_entry`, which signs an existing entry "in place".

    Note that if using the function form of `signer`, the signer is assumed to be
    the entry's credential address. If you need a different key to sign the
    entry, you will need to use different method (e.g., fork this code).

    :param signer: either a :class:`Keypair` or a function which takes a payload
        (a :class:`stellar_xdr.HashIDPreimage` instance) input and returns a bytes signature,
        the signing key should correspond to the address in the `entry`.
    :param public_key: the public identity of the signer (when providing a :class:`Keypair` to `signer`,
        this can be omitted, as it just uses the public key of the keypair)
    :param valid_until_ledger_sequence: the (exclusive) future ledger sequence number until which
        this authorization entry should be valid (if `currentLedgerSeq==validUntil`, this is expired)
    :param invocation: invocation the invocation tree that we're authorizing (likely, this comes from transaction simulation)
    :param network_passphrase: the network passphrase is incorporated into the signature (see :class:`stellar_sdk.Network` for options)
    :return: a signed Soroban authorization entry.
    """
    nonce = random.randint(-(2**63), 2**63 - 1)
    pk = public_key
    if not pk and isinstance(signer, Keypair):
        pk = signer.public_key

    if not pk:
        raise ValueError("`public_key` parameter is required.")

    entry = stellar_xdr.SorobanAuthorizationEntry(
        root_invocation=invocation,
        credentials=stellar_xdr.SorobanCredentials(
            type=stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS,
            address=stellar_xdr.SorobanAddressCredentials(
                address=Address(pk).to_xdr_sc_address(),
                nonce=stellar_xdr.Int64(nonce),
                signature_expiration_ledger=stellar_xdr.Uint32(0),
                signature=stellar_xdr.SCVal(type=stellar_xdr.SCValType.SCV_VOID),
            ),
        ),
    )
    return authorize_entry(
        entry, signer, valid_until_ledger_sequence, network_passphrase
    )
