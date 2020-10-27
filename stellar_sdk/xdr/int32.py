# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .base import *

__all__ = ["Int32"]


class Int32:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef int int32;
    ----------------------------------------------------------------
    """

    def __init__(self, int32: int) -> None:
        self.int32 = int32

    def pack(self, packer: Packer) -> None:
        Integer(self.int32).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Int32":
        int32 = Integer.unpack(unpacker)
        return cls(int32)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "Int32":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Int32":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.int32 == other.int32

    def __str__(self):
        return f"<Int32 [int32={self.int32}]>"
