# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING
from xdrlib3 import Packer, Unpacker
from .base import Integer, UnsignedInteger, Float, Double, Hyper, UnsignedHyper, Boolean, String, Opaque
from .constants import *

from .lots_of_my_structs import LotsOfMyStructs
__all__ = ['HasStuff']
class HasStuff:
    """
    XDR Source Code::

        struct HasStuff
        {
          LotsOfMyStructs data;
        };
    """
    def __init__(
        self,
        data: LotsOfMyStructs,
    ) -> None:
        self.data = data
    def pack(self, packer: Packer) -> None:
        self.data.pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker) -> HasStuff:
        data = LotsOfMyStructs.unpack(unpacker)
        return cls(
            data=data,
        )
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> HasStuff:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> HasStuff:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
    def __hash__(self):
        return hash((self.data,))
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.data== other.data
    def __repr__(self):
        out = [
            f'data={self.data}',
        ]
        return f"<HasStuff [{', '.join(out)}]>"
