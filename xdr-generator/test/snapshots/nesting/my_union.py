# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING
from xdrlib3 import Packer, Unpacker
from .base import Integer, UnsignedInteger, Float, Double, Hyper, UnsignedHyper, Boolean, String, Opaque
from .constants import *

from .union_key import UnionKey
from .my_union_one import MyUnionOne
from .my_union_two import MyUnionTwo
__all__ = ['MyUnion']
class MyUnion:
    """
    XDR Source Code::

        union MyUnion switch (UnionKey type)
        {
            case ONE:
                struct {
                    int someInt;
                } one;

            case TWO:
                struct {
                    int someInt;
                    Foo foo;
                } two;

            case OFFER:
                void;
        };
    """
    def __init__(
        self,
        type: UnionKey,
        one: Optional[MyUnionOne] = None,
        two: Optional[MyUnionTwo] = None,
    ) -> None:
        self.type = type
        self.one = one
        self.two = two
    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == UnionKey.ONE:
            if self.one is None:
                raise ValueError("one should not be None.")
            self.one.pack(packer)
            return
        if self.type == UnionKey.TWO:
            if self.two is None:
                raise ValueError("two should not be None.")
            self.two.pack(packer)
            return
        if self.type == UnionKey.OFFER:
            return
    @classmethod
    def unpack(cls, unpacker: Unpacker) -> MyUnion:
        type = UnionKey.unpack(unpacker)
        if type == UnionKey.ONE:
            one = MyUnionOne.unpack(unpacker)
            return cls(type=type, one=one)
        if type == UnionKey.TWO:
            two = MyUnionTwo.unpack(unpacker)
            return cls(type=type, two=two)
        if type == UnionKey.OFFER:
            return cls(type=type)
        return cls(type=type)
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> MyUnion:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> MyUnion:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
    def __hash__(self):
        return hash((self.type, self.one, self.two,))
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.type== other.type and self.one== other.one and self.two== other.two
    def __repr__(self):
        out = []
        out.append(f'type={self.type}')
        out.append(f'one={self.one}') if self.one is not None else None
        out.append(f'two={self.two}') if self.two is not None else None
        return f"<MyUnion [{', '.join(out)}]>"
