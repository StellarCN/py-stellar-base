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
__all__ = ['Hashes2']
class Hashes2:
    """
    XDR Source Code::

        typedef Hash Hashes2<12>;
    """
    def __init__(self, hashes2: List[Hash]) -> None:
        _expect_max_length = 12
        if hashes2 and len(hashes2) > _expect_max_length:
            raise ValueError(f"The maximum length of `hashes2` should be {_expect_max_length}, but got {len(hashes2)}.")
        self.hashes2 = hashes2
    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.hashes2))
        for hashes2_item in self.hashes2:
            hashes2_item.pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker) -> Hashes2:
        length = unpacker.unpack_uint()
        hashes2 = []
        for _ in range(length):
            hashes2.append(Hash.unpack(unpacker))
        return cls(hashes2)
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Hashes2:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> Hashes2:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
    def __hash__(self):
        return hash(self.hashes2)
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.hashes2 == other.hashes2

    def __repr__(self):
        return f"<Hashes2 [hashes2={self.hashes2}]>"
