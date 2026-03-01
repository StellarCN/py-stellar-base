# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING
from xdrlib3 import Packer, Unpacker
from .base import DEFAULT_XDR_MAX_DEPTH, Integer, UnsignedInteger, Float, Double, Hyper, UnsignedHyper, Boolean, String, Opaque
from .constants import *

from .int64 import Int64
__all__ = ['MyStruct']
class MyStruct:
    """
    XDR Source Code::

        struct MyStruct
        {
            int    someInt;
            int64  aBigInt;
            opaque someOpaque[10];
            string someString<>;
            string maxString<100>;
        };
    """
    def __init__(
        self,
        some_int: int,
        a_big_int: Int64,
        some_opaque: bytes,
        some_string: bytes,
        max_string: bytes,
    ) -> None:
        _expect_length = 10
        if some_opaque and len(some_opaque) != _expect_length:
            raise ValueError(f"The length of `some_opaque` should be {_expect_length}, but got {len(some_opaque)}.")
        _expect_max_length = 4294967295
        if some_string and len(some_string) > _expect_max_length:
            raise ValueError(f"The maximum length of `some_string` should be {_expect_max_length}, but got {len(some_string)}.")
        _expect_max_length = 100
        if max_string and len(max_string) > _expect_max_length:
            raise ValueError(f"The maximum length of `max_string` should be {_expect_max_length}, but got {len(max_string)}.")
        self.some_int = some_int
        self.a_big_int = a_big_int
        self.some_opaque = some_opaque
        self.some_string = some_string
        self.max_string = max_string
    def pack(self, packer: Packer) -> None:
        Integer(self.some_int).pack(packer)
        self.a_big_int.pack(packer)
        Opaque(self.some_opaque, 10, True).pack(packer)
        String(self.some_string, 4294967295).pack(packer)
        String(self.max_string, 100).pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH) -> MyStruct:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        some_int = Integer.unpack(unpacker)
        a_big_int = Int64.unpack(unpacker, depth_limit - 1)
        some_opaque = Opaque.unpack(unpacker, 10, True)
        some_string = String.unpack(unpacker, 4294967295)
        max_string = String.unpack(unpacker, 100)
        return cls(
            some_int=some_int,
            a_big_int=a_big_int,
            some_opaque=some_opaque,
            some_string=some_string,
            max_string=max_string,
        )
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> MyStruct:
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
    def from_xdr(cls, xdr: str) -> MyStruct:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> MyStruct:
        return cls.from_json_dict(json.loads(json_str))
    def to_json_dict(self) -> dict:
        return {
            "some_int": Integer.to_json_dict(self.some_int),
            "a_big_int": self.a_big_int.to_json_dict(),
            "some_opaque": Opaque.to_json_dict(self.some_opaque),
            "some_string": String.to_json_dict(self.some_string),
            "max_string": String.to_json_dict(self.max_string),
        }
    @classmethod
    def from_json_dict(cls, json_dict: dict) -> MyStruct:
        some_int = Integer.from_json_dict(json_dict["some_int"])
        a_big_int = Int64.from_json_dict(json_dict["a_big_int"])
        some_opaque = Opaque.from_json_dict(json_dict["some_opaque"])
        some_string = String.from_json_dict(json_dict["some_string"])
        max_string = String.from_json_dict(json_dict["max_string"])
        return cls(
            some_int=some_int,
            a_big_int=a_big_int,
            some_opaque=some_opaque,
            some_string=some_string,
            max_string=max_string,
        )
    def __hash__(self):
        return hash((self.some_int, self.a_big_int, self.some_opaque, self.some_string, self.max_string,))
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.some_int == other.some_int and self.a_big_int == other.a_big_int and self.some_opaque == other.some_opaque and self.some_string == other.some_string and self.max_string == other.max_string
    def __repr__(self):
        out = [
            f'some_int={self.some_int}',
            f'a_big_int={self.a_big_int}',
            f'some_opaque={self.some_opaque}',
            f'some_string={self.some_string}',
            f'max_string={self.max_string}',
        ]
        return f"<MyStruct [{', '.join(out)}]>"
