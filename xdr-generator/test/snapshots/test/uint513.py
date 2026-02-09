# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING
from xdrlib3 import Packer, Unpacker
from .base import Integer, UnsignedInteger, Float, Double, Hyper, UnsignedHyper, Boolean, String, Opaque
from .constants import *

__all__ = ['Uint513']
class Uint513:
    """
    XDR Source Code::

        typedef opaque uint513<64>;
    """
    def __init__(self, uint513: bytes) -> None:
        self.uint513 = uint513
    def pack(self, packer: Packer) -> None:
        Opaque(self.uint513, 64, False).pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker) -> Uint513:
        uint513 = Opaque.unpack(unpacker, 64, False)
        return cls(uint513)
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Uint513:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> Uint513:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
    def __hash__(self):
        return hash(self.uint513)
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.uint513 == other.uint513

    def __repr__(self):
        return f"<Uint513 [uint513={self.uint513}]>"
