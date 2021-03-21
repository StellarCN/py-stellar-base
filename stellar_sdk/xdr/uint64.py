# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .base import *

__all__ = ["Uint64"]


class Uint64:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef unsigned hyper uint64;
    ----------------------------------------------------------------
    """

    def __init__(self, uint64: int) -> None:

        self.uint64 = uint64

    def pack(self, packer: Packer) -> None:
        UnsignedHyper(self.uint64).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Uint64":
        uint64 = UnsignedHyper.unpack(unpacker)
        return cls(uint64)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "Uint64":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Uint64":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.uint64 == other.uint64

    def __str__(self):
        return f"<Uint64 [uint64={self.uint64}]>"
