# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .sc_address import SCAddress
from .uint64 import Uint64

__all__ = ["AddressWithNonce"]


class AddressWithNonce:
    """
    XDR Source Code::

        struct AddressWithNonce
        {
            SCAddress address;
            uint64 nonce;
        };
    """

    def __init__(
        self,
        address: SCAddress,
        nonce: Uint64,
    ) -> None:
        self.address = address
        self.nonce = nonce

    def pack(self, packer: Packer) -> None:
        self.address.pack(packer)
        self.nonce.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AddressWithNonce":
        address = SCAddress.unpack(unpacker)
        nonce = Uint64.unpack(unpacker)
        return cls(
            address=address,
            nonce=nonce,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "AddressWithNonce":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AddressWithNonce":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.address == other.address and self.nonce == other.nonce

    def __str__(self):
        out = [
            f"address={self.address}",
            f"nonce={self.nonce}",
        ]
        return f"<AddressWithNonce [{', '.join(out)}]>"
