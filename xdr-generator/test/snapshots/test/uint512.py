# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING
from xdrlib3 import Packer, Unpacker
from .base import Integer, UnsignedInteger, Float, Double, Hyper, UnsignedHyper, Boolean, String, Opaque
from .constants import *

__all__ = ['Uint512']
class Uint512:
    """
    XDR Source Code::

        typedef opaque uint512[64];
    """
    def __init__(self, uint512: bytes) -> None:
        self.uint512 = uint512
    def pack(self, packer: Packer) -> None:
        Opaque(self.uint512, 64, True).pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker) -> Uint512:
        uint512 = Opaque.unpack(unpacker, 64, True)
        return cls(uint512)
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Uint512:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> Uint512:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
    def __hash__(self):
        return hash(self.uint512)
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.uint512 == other.uint512

    def __repr__(self):
        return f"<Uint512 [uint512={self.uint512}]>"
