from typing import Callable, Union

from . import scval
from . import xdr as stellar_xdr
from .address import Address
from .exceptions import BadSignatureError
from .keypair import Keypair
from .network import Network
from .utils import sha256

__all__ = ["sign_authorize_entry"]


def sign_authorize_entry(
    entry: stellar_xdr.SorobanAuthorizationEntry,
    signer: Union[Keypair, Callable[[stellar_xdr.SorobanAuthorizationEntry], bytes]],
    valid_until_ledger_sequence: int,
    network_passphrase: str,
) -> stellar_xdr.SorobanAuthorizationEntry:
    if (
        entry.credentials.type
        != stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS
    ):
        return entry

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
    else:
        signature = signer(entry)

    public_key = Address.from_xdr_sc_address(addr_auth.address).key
    try:
        Keypair.from_raw_ed25519_public_key(public_key).verify(payload, signature)
    except BadSignatureError as e:
        raise ValueError("signature doesn't match payload.") from e

    sig_scval = scval.to_map(
        {
            scval.to_symbol("public_key"): scval.to_bytes(public_key),
            scval.to_symbol("signature"): scval.to_bytes(signature),
        }
    )
    addr_auth.signature_args = scval.to_vec([sig_scval])
    return entry
