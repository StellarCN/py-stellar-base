# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING
from xdrlib3 import Packer, Unpacker
from .base import Integer, UnsignedInteger, Float, Double, Hyper, UnsignedHyper, Boolean, String, Opaque
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
    def unpack(cls, unpacker: Unpacker) -> TestArray:
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
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> TestArray:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
    def __hash__(self):
        return hash(self.test_array)
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.test_array == other.test_array

    def __repr__(self):
        return f"<TestArray [test_array={self.test_array}]>"
