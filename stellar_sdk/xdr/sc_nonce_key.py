# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .sc_address import SCAddress

__all__ = ["SCNonceKey"]


class SCNonceKey:
    """
    XDR Source Code::

        struct SCNonceKey {
            SCAddress nonce_address;
        };
    """

    def __init__(
        self,
        nonce_address: SCAddress,
    ) -> None:
        self.nonce_address = nonce_address

    def pack(self, packer: Packer) -> None:
        self.nonce_address.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCNonceKey":
        nonce_address = SCAddress.unpack(unpacker)
        return cls(
            nonce_address=nonce_address,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCNonceKey":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCNonceKey":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.nonce_address == other.nonce_address

    def __str__(self):
        out = [
            f"nonce_address={self.nonce_address}",
        ]
        return f"<SCNonceKey [{', '.join(out)}]>"
