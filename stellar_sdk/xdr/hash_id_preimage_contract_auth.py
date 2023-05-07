# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib3 import Packer, Unpacker

from .authorized_invocation import AuthorizedInvocation
from .hash import Hash
from .uint64 import Uint64

__all__ = ["HashIDPreimageContractAuth"]


class HashIDPreimageContractAuth:
    """
    XDR Source Code::

        struct
            {
                Hash networkID;
                uint64 nonce;
                AuthorizedInvocation invocation;
            }
    """

    def __init__(
        self,
        network_id: Hash,
        nonce: Uint64,
        invocation: AuthorizedInvocation,
    ) -> None:
        self.network_id = network_id
        self.nonce = nonce
        self.invocation = invocation

    def pack(self, packer: Packer) -> None:
        self.network_id.pack(packer)
        self.nonce.pack(packer)
        self.invocation.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "HashIDPreimageContractAuth":
        network_id = Hash.unpack(unpacker)
        nonce = Uint64.unpack(unpacker)
        invocation = AuthorizedInvocation.unpack(unpacker)
        return cls(
            network_id=network_id,
            nonce=nonce,
            invocation=invocation,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "HashIDPreimageContractAuth":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "HashIDPreimageContractAuth":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.network_id == other.network_id
            and self.nonce == other.nonce
            and self.invocation == other.invocation
        )

    def __str__(self):
        out = [
            f"network_id={self.network_id}",
            f"nonce={self.nonce}",
            f"invocation={self.invocation}",
        ]
        return f"<HashIDPreimageContractAuth [{', '.join(out)}]>"
