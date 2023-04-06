from typing import Optional, Union, Sequence

from .authorized_invocation import AuthorizedInvocation
from .. import xdr as stellar_xdr
from ..keypair import Keypair
from ..network import Network
from ..soroban.types import BaseScValAlias, AccountEd25519Signature
from ..soroban.types.address import Address
from ..utils import sha256

__all__ = ["ContractAuth"]


class ContractAuth:
    """Represents a contract authorization.

    See `Soroban Documentation - Authorization <https://soroban.stellar.org/docs/learn/authorization>`_
        for more information.

    :param address: The address, must be set if nonce is set.
    :param nonce: The nonce, must be set if address is set.
    :param root_invocation: The root invocation.
    :param signature_args: The signature arguments.
    """

    def __init__(
        self,
        address: Optional[Address],
        nonce: Optional[int],
        root_invocation: AuthorizedInvocation,
        signature_args: Optional[
            Sequence[Union[BaseScValAlias, stellar_xdr.SCVal]]
        ] = None,
    ):
        if (address and nonce is None) or (not address and nonce is not None):
            raise ValueError("address and nonce must both be set or both be None")
        self.address = address
        self.nonce = nonce
        self.root_invocation = root_invocation
        self.signature_args = []
        if signature_args:
            self.signature_args = [
                arg.to_xdr_sc_val() if isinstance(arg, BaseScValAlias) else arg
                for arg in signature_args
            ]

    def sign(self, signer: Keypair, network_passphrase: str) -> None:
        """Sign the contract authorization, the signature will be added to the `signature_args`.

        For custom accounts, this signature format may not be applicable.

        :param signer: The signer.
        """
        if self.address is None or self.nonce is None:
            raise ValueError("`address` and `nonce` must be set.")
        network_id = Network(network_passphrase).network_id()
        root_invocation_preimage = (
            stellar_xdr.HashIDPreimage.from_envelope_type_contract_auth(
                stellar_xdr.HashIDPreimageContractAuth(
                    network_id=stellar_xdr.Hash(network_id),
                    nonce=stellar_xdr.Uint64(self.nonce),
                    invocation=self.root_invocation.to_xdr_object(),
                )
            ).to_xdr_bytes()
        )
        payload = sha256(root_invocation_preimage)
        signature_bytes = signer.sign(payload)
        signature = AccountEd25519Signature(
            signer.public_key, signature_bytes
        ).to_xdr_sc_val()
        self.signature_args.append(signature)

    def to_xdr_object(self) -> stellar_xdr.ContractAuth:
        address_with_nonce = None
        if self.address:
            assert self.nonce is not None
            address_with_nonce = stellar_xdr.AddressWithNonce(
                address=self.address.to_xdr_sc_address(),
                nonce=stellar_xdr.Uint64(self.nonce),
            )
        if self.signature_args:
            # TODO: https://discord.com/channels/897514728459468821/1076723574884282398/1078095366890729595
            signature_args = stellar_xdr.SCVec(
                [stellar_xdr.SCVal.from_scv_vec(stellar_xdr.SCVec(self.signature_args))]
            )
        else:
            signature_args = stellar_xdr.SCVec([])
        return stellar_xdr.ContractAuth(
            address_with_nonce=address_with_nonce,
            root_invocation=self.root_invocation.to_xdr_object(),
            signature_args=signature_args,
        )

    @classmethod
    def from_xdr_object(cls, xdr_object: stellar_xdr.ContractAuth) -> "ContractAuth":
        address = None
        nonce = None
        if xdr_object.address_with_nonce:
            address = Address.from_xdr_sc_address(xdr_object.address_with_nonce.address)
            nonce = xdr_object.address_with_nonce.nonce.uint64
        root_invocation = AuthorizedInvocation.from_xdr_object(
            xdr_object.root_invocation
        )
        signature_args = xdr_object.signature_args.sc_vec
        return cls(address, nonce, root_invocation, signature_args)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.address == other.address
            and self.nonce == other.nonce
            and self.root_invocation == other.root_invocation
            and self.signature_args == other.signature_args
        )

    def __str__(self):
        return f"<ContractAuth [address={self.address}, nonce={self.nonce}, root_invocation={self.root_invocation}, signature_args={self.signature_args}]>"
