# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING
from xdrlib3 import Packer, Unpacker
from .base import Integer, UnsignedInteger, Float, Double, Hyper, UnsignedHyper, Boolean, String, Opaque
from .constants import *

__all__ = ['Str2']
class Str2:
    """
    XDR Source Code::

        typedef string str2<>;
    """
    def __init__(self, str2: bytes) -> None:
        self.str2 = str2
    def pack(self, packer: Packer) -> None:
        String(self.str2, 4294967295).pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker) -> Str2:
        str2 = String.unpack(unpacker)
        return cls(str2)
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Str2:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> Str2:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
    def __hash__(self):
        return hash(self.str2)
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.str2 == other.str2

    def __repr__(self):
        return f"<Str2 [str2={self.str2}]>"
