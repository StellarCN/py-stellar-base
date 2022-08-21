# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from enum import IntEnum
from xdrlib import Packer, Unpacker

__all__ = ["SCSpecType"]


class SCSpecType(IntEnum):
    """
    XDR Source Code::

        enum SCSpecType
        {
            // Types with no parameters.
            SC_SPEC_TYPE_U32 = 1,
            SC_SPEC_TYPE_I32 = 2,
            SC_SPEC_TYPE_U64 = 3,
            SC_SPEC_TYPE_I64 = 4,
            SC_SPEC_TYPE_BOOL = 5,
            SC_SPEC_TYPE_SYMBOL = 6,
            SC_SPEC_TYPE_BITSET = 7,
            SC_SPEC_TYPE_STATUS = 8,
            SC_SPEC_TYPE_BYTES = 9,
            SC_SPEC_TYPE_BIG_INT = 10,

            // Types with parameters.
            SC_SPEC_TYPE_OPTION = 1000,
            SC_SPEC_TYPE_RESULT = 1001,
            SC_SPEC_TYPE_VEC = 1002,
            SC_SPEC_TYPE_SET = 1003,
            SC_SPEC_TYPE_MAP = 1004,
            SC_SPEC_TYPE_TUPLE = 1005,

            // User defined types.
            SC_SPEC_TYPE_UDT = 2000
        };
    """

    SC_SPEC_TYPE_U32 = 1
    SC_SPEC_TYPE_I32 = 2
    SC_SPEC_TYPE_U64 = 3
    SC_SPEC_TYPE_I64 = 4
    SC_SPEC_TYPE_BOOL = 5
    SC_SPEC_TYPE_SYMBOL = 6
    SC_SPEC_TYPE_BITSET = 7
    SC_SPEC_TYPE_STATUS = 8
    SC_SPEC_TYPE_BYTES = 9
    SC_SPEC_TYPE_BIG_INT = 10
    SC_SPEC_TYPE_OPTION = 1000
    SC_SPEC_TYPE_RESULT = 1001
    SC_SPEC_TYPE_VEC = 1002
    SC_SPEC_TYPE_SET = 1003
    SC_SPEC_TYPE_MAP = 1004
    SC_SPEC_TYPE_TUPLE = 1005
    SC_SPEC_TYPE_UDT = 2000

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCSpecType":
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCSpecType":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCSpecType":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
