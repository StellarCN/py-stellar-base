# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING
from xdrlib3 import Packer, Unpacker
from .base import Integer, UnsignedInteger, Float, Double, Hyper, UnsignedHyper, Boolean, String, Opaque
from .constants import *

from .color import Color
__all__ = ['NesterNestedUnion']
class NesterNestedUnion:
    """
    XDR Source Code::

        union switch (Color color) {
            case RED:
              void;
            default:
              int blah2;
          }
    """
    def __init__(
        self,
        color: Color,
        blah2: Optional[int] = None,
    ) -> None:
        self.color = color
        self.blah2 = blah2
    def pack(self, packer: Packer) -> None:
        self.color.pack(packer)
        if self.color == Color.RED:
            return
        if self.blah2 is None:
            raise ValueError("blah2 should not be None.")
        Integer(self.blah2).pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker) -> NesterNestedUnion:
        color = Color.unpack(unpacker)
        if color == Color.RED:
            return cls(color=color)
        blah2 = Integer.unpack(unpacker)
        return cls(color=color, blah2=blah2)
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> NesterNestedUnion:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> NesterNestedUnion:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
    def __hash__(self):
        return hash((self.color, self.blah2,))
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.color== other.color and self.blah2== other.blah2
    def __repr__(self):
        out = []
        out.append(f'color={self.color}')
        out.append(f'blah2={self.blah2}') if self.blah2 is not None else None
        return f"<NesterNestedUnion [{', '.join(out)}]>"
