# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from enum import IntEnum
from xdrlib import Packer, Unpacker

__all__ = ["SCValType"]


class SCValType(IntEnum):
    """
    XDR Source Code::

        enum SCValType
        {
            SCV_U63 = 0,
            SCV_U32 = 1,
            SCV_I32 = 2,
            SCV_STATIC = 3,
            SCV_OBJECT = 4,
            SCV_SYMBOL = 5,
            SCV_BITSET = 6,
            SCV_STATUS = 7
        };
    """

    SCV_U63 = 0
    SCV_U32 = 1
    SCV_I32 = 2
    SCV_STATIC = 3
    SCV_OBJECT = 4
    SCV_SYMBOL = 5
    SCV_BITSET = 6
    SCV_STATUS = 7

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCValType":
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCValType":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCValType":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
