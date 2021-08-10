# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .base import Opaque

__all__ = ["Uint256"]


class Uint256:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef opaque uint256[32];
    ----------------------------------------------------------------
    """

    def __init__(self, uint256: bytes) -> None:
        self.uint256 = uint256

    def pack(self, packer: Packer) -> None:
        Opaque(self.uint256, 32, True).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Uint256":
        uint256 = Opaque.unpack(unpacker, 32, True)
        return cls(uint256)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "Uint256":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Uint256":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.uint256 == other.uint256

    def __str__(self):
        return f"<Uint256 [uint256={self.uint256}]>"
