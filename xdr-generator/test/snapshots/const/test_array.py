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

__all__ = ['TestArray']
class TestArray:
    """
    XDR Source Code::

        typedef int TestArray[FOO];
    """
    def __init__(self, test_array: List[int]) -> None:
        _expect_length = FOO
        if test_array and len(test_array) != _expect_length:
            raise ValueError(f"The length of `test_array` should be {_expect_length}, but got {len(test_array)}.")
        self.test_array = test_array
    def pack(self, packer: Packer) -> None:
        for test_array_item in self.test_array:
            Integer(test_array_item).pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH) -> TestArray:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        length = FOO
        test_array = []
        for _ in range(length):
            test_array.append(Integer.unpack(unpacker))
        return cls(test_array)
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TestArray:
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
    def from_xdr(cls, xdr: str) -> TestArray:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TestArray:
        return cls.from_json_dict(json.loads(json_str))
    def to_json_dict(self):
        return [Integer.to_json_dict(item) for item in self.test_array]
    @classmethod
    def from_json_dict(cls, json_value: list) -> TestArray:
        return cls([Integer.from_json_dict(item) for item in json_value])
    def __hash__(self):
        return hash((self.test_array,))
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.test_array == other.test_array
    def __repr__(self):
        return f"<TestArray [test_array={self.test_array}]>"
