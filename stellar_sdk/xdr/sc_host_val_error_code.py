# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from enum import IntEnum
from xdrlib import Packer, Unpacker

__all__ = ["SCHostValErrorCode"]


class SCHostValErrorCode(IntEnum):
    """
    XDR Source Code::

        enum SCHostValErrorCode
        {
            HOST_VALUE_UNKNOWN_ERROR = 0,
            HOST_VALUE_RESERVED_TAG_VALUE = 1,
            HOST_VALUE_UNEXPECTED_VAL_TYPE = 2,
            HOST_VALUE_U63_OUT_OF_RANGE = 3,
            HOST_VALUE_U32_OUT_OF_RANGE = 4,
            HOST_VALUE_STATIC_UNKNOWN = 5,
            HOST_VALUE_MISSING_OBJECT = 6,
            HOST_VALUE_SYMBOL_TOO_LONG = 7,
            HOST_VALUE_SYMBOL_BAD_CHAR = 8,
            HOST_VALUE_SYMBOL_CONTAINS_NON_UTF8 = 9,
            HOST_VALUE_BITSET_TOO_MANY_BITS = 10,
            HOST_VALUE_STATUS_UNKNOWN = 11
        };
    """

    HOST_VALUE_UNKNOWN_ERROR = 0
    HOST_VALUE_RESERVED_TAG_VALUE = 1
    HOST_VALUE_UNEXPECTED_VAL_TYPE = 2
    HOST_VALUE_U63_OUT_OF_RANGE = 3
    HOST_VALUE_U32_OUT_OF_RANGE = 4
    HOST_VALUE_STATIC_UNKNOWN = 5
    HOST_VALUE_MISSING_OBJECT = 6
    HOST_VALUE_SYMBOL_TOO_LONG = 7
    HOST_VALUE_SYMBOL_BAD_CHAR = 8
    HOST_VALUE_SYMBOL_CONTAINS_NON_UTF8 = 9
    HOST_VALUE_BITSET_TOO_MANY_BITS = 10
    HOST_VALUE_STATUS_UNKNOWN = 11

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCHostValErrorCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCHostValErrorCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCHostValErrorCode":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
