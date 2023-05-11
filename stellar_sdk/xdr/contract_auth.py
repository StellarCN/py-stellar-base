# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import Optional
from xdrlib3 import Packer, Unpacker

from .address_with_nonce import AddressWithNonce
from .authorized_invocation import AuthorizedInvocation
from .sc_vec import SCVec

__all__ = ["ContractAuth"]


class ContractAuth:
    """
    XDR Source Code::

        struct ContractAuth
        {
            AddressWithNonce* addressWithNonce; // not present for invoker
            AuthorizedInvocation rootInvocation;
            SCVec signatureArgs;
        };
    """

    def __init__(
        self,
        address_with_nonce: Optional[AddressWithNonce],
        root_invocation: AuthorizedInvocation,
        signature_args: SCVec,
    ) -> None:
        self.address_with_nonce = address_with_nonce
        self.root_invocation = root_invocation
        self.signature_args = signature_args

    def pack(self, packer: Packer) -> None:
        if self.address_with_nonce is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.address_with_nonce.pack(packer)
        self.root_invocation.pack(packer)
        self.signature_args.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ContractAuth":
        address_with_nonce = (
            AddressWithNonce.unpack(unpacker) if unpacker.unpack_uint() else None
        )
        root_invocation = AuthorizedInvocation.unpack(unpacker)
        signature_args = SCVec.unpack(unpacker)
        return cls(
            address_with_nonce=address_with_nonce,
            root_invocation=root_invocation,
            signature_args=signature_args,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "ContractAuth":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ContractAuth":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.address_with_nonce == other.address_with_nonce
            and self.root_invocation == other.root_invocation
            and self.signature_args == other.signature_args
        )

    def __str__(self):
        out = [
            f"address_with_nonce={self.address_with_nonce}",
            f"root_invocation={self.root_invocation}",
            f"signature_args={self.signature_args}",
        ]
        return f"<ContractAuth [{', '.join(out)}]>"
