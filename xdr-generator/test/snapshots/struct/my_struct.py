# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING
from xdrlib3 import Packer, Unpacker
from .base import Integer, UnsignedInteger, Float, Double, Hyper, UnsignedHyper, Boolean, String, Opaque
from .constants import *

from .int64 import Int64
__all__ = ['MyStruct']
class MyStruct:
    """
    XDR Source Code::

        struct MyStruct
        {
            int    someInt;
            int64  aBigInt;
            opaque someOpaque[10];
            string someString<>;
            string maxString<100>;
        };
    """
    def __init__(
        self,
        some_int: int,
        a_big_int: Int64,
        some_opaque: bytes,
        some_string: bytes,
        max_string: bytes,
    ) -> None:
        self.some_int = some_int
        self.a_big_int = a_big_int
        self.some_opaque = some_opaque
        self.some_string = some_string
        self.max_string = max_string
    def pack(self, packer: Packer) -> None:
        Integer(self.some_int).pack(packer)
        self.a_big_int.pack(packer)
        Opaque(self.some_opaque, 10, True).pack(packer)
        String(self.some_string, 4294967295).pack(packer)
        String(self.max_string, 100).pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker) -> MyStruct:
        some_int = Integer.unpack(unpacker)
        a_big_int = Int64.unpack(unpacker)
        some_opaque = Opaque.unpack(unpacker, 10, True)
        some_string = String.unpack(unpacker)
        max_string = String.unpack(unpacker)
        return cls(
            some_int=some_int,
            a_big_int=a_big_int,
            some_opaque=some_opaque,
            some_string=some_string,
            max_string=max_string,
        )
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> MyStruct:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> MyStruct:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
    def __hash__(self):
        return hash((self.some_int, self.a_big_int, self.some_opaque, self.some_string, self.max_string,))
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.some_int== other.some_int and self.a_big_int== other.a_big_int and self.some_opaque== other.some_opaque and self.some_string== other.some_string and self.max_string== other.max_string
    def __repr__(self):
        out = [
            f'some_int={self.some_int}',
            f'a_big_int={self.a_big_int}',
            f'some_opaque={self.some_opaque}',
            f'some_string={self.some_string}',
            f'max_string={self.max_string}',
        ]
        return f"<MyStruct [{', '.join(out)}]>"
