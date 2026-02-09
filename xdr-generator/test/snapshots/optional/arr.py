# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING
from xdrlib3 import Packer, Unpacker
from .base import Integer, UnsignedInteger, Float, Double, Hyper, UnsignedHyper, Boolean, String, Opaque
from .constants import *

__all__ = ['Arr']
class Arr:
    """
    XDR Source Code::

        typedef int Arr[2];
    """
    def __init__(self, arr: List[int]) -> None:
        _expect_length = 2
        if arr and len(arr) != _expect_length:
            raise ValueError(f"The length of `arr` should be {_expect_length}, but got {len(arr)}.")
        self.arr = arr
    def pack(self, packer: Packer) -> None:
        for arr_item in self.arr:
            Integer(arr_item).pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker) -> Arr:
        length = 2
        arr = []
        for _ in range(length):
            arr.append(Integer.unpack(unpacker))
        return cls(arr)
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Arr:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> Arr:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
    def __hash__(self):
        return hash(self.arr)
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.arr == other.arr

    def __repr__(self):
        return f"<Arr [arr={self.arr}]>"
