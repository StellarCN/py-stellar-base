# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING
from xdrlib3 import Packer, Unpacker
from .base import DEFAULT_XDR_MAX_DEPTH, Integer, UnsignedInteger, Float, Double, Hyper, UnsignedHyper, Boolean, String, Opaque
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
        raise ValueError("Invalid type.")
    @classmethod
    def unpack(cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH) -> MyUnion:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = UnionKey.unpack(unpacker)
        if type == UnionKey.ONE:
            one = MyUnionOne.unpack(unpacker, depth_limit - 1)
            return cls(type=type, one=one)
        if type == UnionKey.TWO:
            two = MyUnionTwo.unpack(unpacker, depth_limit - 1)
            return cls(type=type, two=two)
        if type == UnionKey.OFFER:
            return cls(type=type)
        raise ValueError("Invalid type.")
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> MyUnion:
        unpacker = Unpacker(xdr)
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> MyUnion:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> MyUnion:
        return cls.from_json_dict(json.loads(json_str))
    def to_json_dict(self):
        if self.type == UnionKey.ONE:
            assert self.one is not None
            return {"one": self.one.to_json_dict()}
        if self.type == UnionKey.TWO:
            assert self.two is not None
            return {"two": self.two.to_json_dict()}
        if self.type == UnionKey.OFFER:
            return "offer"
        raise ValueError(f"Unknown type in MyUnion: {self.type}")
    @classmethod
    def from_json_dict(cls, json_value: str | dict) -> MyUnion:
        if isinstance(json_value, str):
            if json_value not in ("offer",):
                raise ValueError(f"Unexpected string '{json_value}' for MyUnion, must be one of: offer")
            type = UnionKey.from_json_dict(json_value)
            return cls(type=type)
        if not isinstance(json_value, dict) or len(json_value) != 1:
            raise ValueError(f"Expected a single-key object for MyUnion, got: {json_value}")
        key = next(iter(json_value))
        type = UnionKey.from_json_dict(key)
        if key == "one":
            one = MyUnionOne.from_json_dict(json_value["one"])
            return cls(type=type, one=one)
        if key == "two":
            two = MyUnionTwo.from_json_dict(json_value["two"])
            return cls(type=type, two=two)
        raise ValueError(f"Unknown key '{key}' for MyUnion")
    def __hash__(self):
        return hash((self.type, self.one, self.two,))
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.type == other.type and self.one == other.one and self.two == other.two
    def __repr__(self):
        out = []
        out.append(f'type={self.type}')
        if self.one is not None:
            out.append(f'one={self.one}')
        if self.two is not None:
            out.append(f'two={self.two}')
        return f"<MyUnion [{', '.join(out)}]>"
