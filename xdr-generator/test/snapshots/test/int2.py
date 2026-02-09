# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING
from xdrlib3 import Packer, Unpacker
from .base import Integer, UnsignedInteger, Float, Double, Hyper, UnsignedHyper, Boolean, String, Opaque
from .constants import *

__all__ = ['Int2']
class Int2:
    """
    XDR Source Code::

        typedef hyper           int2;
    """
    def __init__(self, int2: int) -> None:
        self.int2 = int2
    def pack(self, packer: Packer) -> None:
        Hyper(self.int2).pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker) -> Int2:
        int2 = Hyper.unpack(unpacker)
        return cls(int2)
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Int2:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> Int2:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
    def __hash__(self):
        return hash(self.int2)
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.int2 == other.int2

    def __repr__(self):
        return f"<Int2 [int2={self.int2}]>"
