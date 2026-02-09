# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING
from xdrlib3 import Packer, Unpacker
from .base import Integer, UnsignedInteger, Float, Double, Hyper, UnsignedHyper, Boolean, String, Opaque
from .constants import *

from .hash import Hash
__all__ = ['OptHash1']
class OptHash1:
    """
    XDR Source Code::

        typedef Hash *optHash1;
    """
    def __init__(self, opt_hash1: Optional[Hash]) -> None:
        self.opt_hash1 = opt_hash1
    def pack(self, packer: Packer) -> None:
        if self.opt_hash1 is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.opt_hash1.pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker) -> OptHash1:
        opt_hash1 = Hash.unpack(unpacker) if unpacker.unpack_uint() else None
        return cls(opt_hash1)
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> OptHash1:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> OptHash1:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
    def __hash__(self):
        return hash(self.opt_hash1)
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.opt_hash1 == other.opt_hash1

    def __repr__(self):
        return f"<OptHash1 [opt_hash1={self.opt_hash1}]>"
