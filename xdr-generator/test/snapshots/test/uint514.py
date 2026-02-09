# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING
from xdrlib3 import Packer, Unpacker
from .base import Integer, UnsignedInteger, Float, Double, Hyper, UnsignedHyper, Boolean, String, Opaque
from .constants import *

__all__ = ['Uint514']
class Uint514:
    """
    XDR Source Code::

        typedef opaque uint514<>;
    """
    def __init__(self, uint514: bytes) -> None:
        self.uint514 = uint514
    def pack(self, packer: Packer) -> None:
        Opaque(self.uint514, 4294967295, False).pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker) -> Uint514:
        uint514 = Opaque.unpack(unpacker, 4294967295, False)
        return cls(uint514)
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Uint514:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> Uint514:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
    def __hash__(self):
        return hash(self.uint514)
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.uint514 == other.uint514

    def __repr__(self):
        return f"<Uint514 [uint514={self.uint514}]>"
