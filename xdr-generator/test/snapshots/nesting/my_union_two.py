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

from .foo import Foo
__all__ = ['MyUnionTwo']
class MyUnionTwo:
    """
    XDR Source Code::

        struct {
                    int someInt;
                    Foo foo;
                }
    """
    def __init__(
        self,
        some_int: int,
        foo: Foo,
    ) -> None:
        self.some_int = some_int
        self.foo = foo
    def pack(self, packer: Packer) -> None:
        Integer(self.some_int).pack(packer)
        self.foo.pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH) -> MyUnionTwo:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        some_int = Integer.unpack(unpacker)
        foo = Foo.unpack(unpacker, depth_limit - 1)
        return cls(
            some_int=some_int,
            foo=foo,
        )
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> MyUnionTwo:
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
    def from_xdr(cls, xdr: str) -> MyUnionTwo:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> MyUnionTwo:
        return cls.from_json_dict(json.loads(json_str))
    def to_json_dict(self) -> dict:
        return {
            "some_int": Integer.to_json_dict(self.some_int),
            "foo": self.foo.to_json_dict(),
        }
    @classmethod
    def from_json_dict(cls, json_dict: dict) -> MyUnionTwo:
        some_int = Integer.from_json_dict(json_dict["some_int"])
        foo = Foo.from_json_dict(json_dict["foo"])
        return cls(
            some_int=some_int,
            foo=foo,
        )
    def __hash__(self):
        return hash((self.some_int, self.foo,))
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.some_int == other.some_int and self.foo == other.foo
    def __repr__(self):
        out = [
            f'some_int={self.some_int}',
            f'foo={self.foo}',
        ]
        return f"<MyUnionTwo [{', '.join(out)}]>"
