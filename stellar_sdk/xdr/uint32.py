# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .base import *

__all__ = ["Uint32"]


class Uint32:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef unsigned int uint32;
    ----------------------------------------------------------------
    """

    def __init__(self, uint32: int) -> None:
        self.uint32 = uint32

    def pack(self, packer: Packer) -> None:
        UnsignedInteger(self.uint32).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Uint32":
        uint32 = UnsignedInteger.unpack(unpacker)
        return cls(uint32)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "Uint32":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Uint32":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.uint32 == other.uint32

    def __str__(self):
        return f"<Uint32 [uint32={self.uint32}]>"
