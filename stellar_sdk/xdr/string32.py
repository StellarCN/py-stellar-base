# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .base import *

__all__ = ["String32"]


class String32:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef string string32<32>;
    ----------------------------------------------------------------
    """

    def __init__(self, string32: bytes) -> None:
        self.string32 = string32

    def pack(self, packer: Packer) -> None:
        String(self.string32, 32).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "String32":
        string32 = String.unpack(unpacker)
        return cls(string32)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "String32":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "String32":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.string32 == other.string32

    def __str__(self):
        return f"<String32 [string32={self.string32}]>"
