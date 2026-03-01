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
    def unpack(cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH) -> NesterNestedUnion:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> NesterNestedUnion:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> NesterNestedUnion:
        return cls.from_json_dict(json.loads(json_str))
    def to_json_dict(self):
        if self.color == Color.RED:
            return "red"
        assert self.blah2 is not None
        return {self.color.to_json_dict(): Integer.to_json_dict(self.blah2)}
    @classmethod
    def from_json_dict(cls, json_value: str | dict) -> NesterNestedUnion:
        if isinstance(json_value, str):
            if json_value not in ("red",):
                raise ValueError(f"Unexpected string '{json_value}' for NesterNestedUnion, must be one of: red")
            color = Color.from_json_dict(json_value)
            return cls(color=color)
        if not isinstance(json_value, dict) or len(json_value) != 1:
            raise ValueError(f"Expected a single-key object for NesterNestedUnion, got: {json_value}")
        key = next(iter(json_value))
        color = Color.from_json_dict(key)
        blah2 = Integer.from_json_dict(json_value[key])
        return cls(color=color, blah2=blah2)
    def __hash__(self):
        return hash((self.color, self.blah2,))
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.color == other.color and self.blah2 == other.blah2
    def __repr__(self):
        out = []
        out.append(f'color={self.color}')
        if self.blah2 is not None:
            out.append(f'blah2={self.blah2}')
        return f"<NesterNestedUnion [{', '.join(out)}]>"
