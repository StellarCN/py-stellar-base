# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING
from xdrlib3 import Packer, Unpacker
from .base import Integer, UnsignedInteger, Float, Double, Hyper, UnsignedHyper, Boolean, String, Opaque
from .constants import *

__all__ = ['MyUnionOne']
class MyUnionOne:
    """
    XDR Source Code::

        struct {
                    int someInt;
                }
    """
    def __init__(
        self,
        some_int: int,
    ) -> None:
        self.some_int = some_int
    def pack(self, packer: Packer) -> None:
        Integer(self.some_int).pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker) -> MyUnionOne:
        some_int = Integer.unpack(unpacker)
        return cls(
            some_int=some_int,
        )
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> MyUnionOne:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> MyUnionOne:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
    def __hash__(self):
        return hash((self.some_int,))
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.some_int== other.some_int
    def __repr__(self):
        out = [
            f'some_int={self.some_int}',
        ]
        return f"<MyUnionOne [{', '.join(out)}]>"
