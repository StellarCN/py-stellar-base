# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .base import *

__all__ = ["Value"]


class Value:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef opaque Value<>;
    ----------------------------------------------------------------
    """

    def __init__(self, value: bytes) -> None:

        self.value = value

    def pack(self, packer: Packer) -> None:
        Opaque(self.value, 4294967295, False).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Value":
        value = Opaque.unpack(unpacker, 4294967295, False)
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "Value":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Value":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    def __str__(self):
        return f"<Value [value={self.value}]>"
