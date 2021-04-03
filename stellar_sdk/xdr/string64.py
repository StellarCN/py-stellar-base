# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .base import *

__all__ = ["String64"]


class String64:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef string string64<64>;
    ----------------------------------------------------------------
    """

    def __init__(self, string64: bytes) -> None:

        self.string64 = string64

    def pack(self, packer: Packer) -> None:
        String(self.string64, 64).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "String64":
        string64 = String.unpack(unpacker)
        return cls(string64)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "String64":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "String64":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.string64 == other.string64

    def __str__(self):
        return f"<String64 [string64={self.string64}]>"
