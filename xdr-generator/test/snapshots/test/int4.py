# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING
from xdrlib3 import Packer, Unpacker
from .base import Integer, UnsignedInteger, Float, Double, Hyper, UnsignedHyper, Boolean, String, Opaque
from .constants import *

__all__ = ['Int4']
class Int4:
    """
    XDR Source Code::

        typedef unsigned hyper  int4;
    """
    def __init__(self, int4: int) -> None:
        self.int4 = int4
    def pack(self, packer: Packer) -> None:
        UnsignedHyper(self.int4).pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker) -> Int4:
        int4 = UnsignedHyper.unpack(unpacker)
        return cls(int4)
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Int4:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> Int4:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
    def __hash__(self):
        return hash(self.int4)
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.int4 == other.int4

    def __repr__(self):
        return f"<Int4 [int4={self.int4}]>"
