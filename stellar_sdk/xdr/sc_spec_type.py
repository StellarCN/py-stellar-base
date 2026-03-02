# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_SC_SPEC_TYPE_MAP = {
    0: "val",
    1: "bool",
    2: "void",
    3: "error",
    4: "u32",
    5: "i32",
    6: "u64",
    7: "i64",
    8: "timepoint",
    9: "duration",
    10: "u128",
    11: "i128",
    12: "u256",
    13: "i256",
    14: "bytes",
    16: "string",
    17: "symbol",
    19: "address",
    20: "muxed_address",
    1000: "option",
    1001: "result",
    1002: "vec",
    1004: "map",
    1005: "tuple",
    1006: "bytes_n",
    2000: "udt",
}
_SC_SPEC_TYPE_REVERSE_MAP = {
    "val": 0,
    "bool": 1,
    "void": 2,
    "error": 3,
    "u32": 4,
    "i32": 5,
    "u64": 6,
    "i64": 7,
    "timepoint": 8,
    "duration": 9,
    "u128": 10,
    "i128": 11,
    "u256": 12,
    "i256": 13,
    "bytes": 14,
    "string": 16,
    "symbol": 17,
    "address": 19,
    "muxed_address": 20,
    "option": 1000,
    "result": 1001,
    "vec": 1002,
    "map": 1004,
    "tuple": 1005,
    "bytes_n": 1006,
    "udt": 2000,
}
__all__ = ["SCSpecType"]


class SCSpecType(IntEnum):
    """
    XDR Source Code::

        enum SCSpecType
        {
            SC_SPEC_TYPE_VAL = 0,

            // Types with no parameters.
            SC_SPEC_TYPE_BOOL = 1,
            SC_SPEC_TYPE_VOID = 2,
            SC_SPEC_TYPE_ERROR = 3,
            SC_SPEC_TYPE_U32 = 4,
            SC_SPEC_TYPE_I32 = 5,
            SC_SPEC_TYPE_U64 = 6,
            SC_SPEC_TYPE_I64 = 7,
            SC_SPEC_TYPE_TIMEPOINT = 8,
            SC_SPEC_TYPE_DURATION = 9,
            SC_SPEC_TYPE_U128 = 10,
            SC_SPEC_TYPE_I128 = 11,
            SC_SPEC_TYPE_U256 = 12,
            SC_SPEC_TYPE_I256 = 13,
            SC_SPEC_TYPE_BYTES = 14,
            SC_SPEC_TYPE_STRING = 16,
            SC_SPEC_TYPE_SYMBOL = 17,
            SC_SPEC_TYPE_ADDRESS = 19,
            SC_SPEC_TYPE_MUXED_ADDRESS = 20,

            // Types with parameters.
            SC_SPEC_TYPE_OPTION = 1000,
            SC_SPEC_TYPE_RESULT = 1001,
            SC_SPEC_TYPE_VEC = 1002,
            SC_SPEC_TYPE_MAP = 1004,
            SC_SPEC_TYPE_TUPLE = 1005,
            SC_SPEC_TYPE_BYTES_N = 1006,

            // User defined types.
            SC_SPEC_TYPE_UDT = 2000
        };
    """

    SC_SPEC_TYPE_VAL = 0
    SC_SPEC_TYPE_BOOL = 1
    SC_SPEC_TYPE_VOID = 2
    SC_SPEC_TYPE_ERROR = 3
    SC_SPEC_TYPE_U32 = 4
    SC_SPEC_TYPE_I32 = 5
    SC_SPEC_TYPE_U64 = 6
    SC_SPEC_TYPE_I64 = 7
    SC_SPEC_TYPE_TIMEPOINT = 8
    SC_SPEC_TYPE_DURATION = 9
    SC_SPEC_TYPE_U128 = 10
    SC_SPEC_TYPE_I128 = 11
    SC_SPEC_TYPE_U256 = 12
    SC_SPEC_TYPE_I256 = 13
    SC_SPEC_TYPE_BYTES = 14
    SC_SPEC_TYPE_STRING = 16
    SC_SPEC_TYPE_SYMBOL = 17
    SC_SPEC_TYPE_ADDRESS = 19
    SC_SPEC_TYPE_MUXED_ADDRESS = 20
    SC_SPEC_TYPE_OPTION = 1000
    SC_SPEC_TYPE_RESULT = 1001
    SC_SPEC_TYPE_VEC = 1002
    SC_SPEC_TYPE_MAP = 1004
    SC_SPEC_TYPE_TUPLE = 1005
    SC_SPEC_TYPE_BYTES_N = 1006
    SC_SPEC_TYPE_UDT = 2000

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCSpecType:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCSpecType:
        unpacker = Unpacker(xdr)
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCSpecType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCSpecType:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _SC_SPEC_TYPE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> SCSpecType:
        return cls(_SC_SPEC_TYPE_REVERSE_MAP[json_value])
