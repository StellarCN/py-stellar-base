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

from .int_union import IntUnion
__all__ = ['IntUnion2']
class IntUnion2:
    """
    XDR Source Code::

        typedef IntUnion IntUnion2;
    """
    def __init__(self, int_union2: IntUnion) -> None:
        self.int_union2 = int_union2
    def pack(self, packer: Packer) -> None:
        self.int_union2.pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH) -> IntUnion2:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        int_union2 = IntUnion.unpack(unpacker, depth_limit - 1)
        return cls(int_union2)
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> IntUnion2:
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
    def from_xdr(cls, xdr: str) -> IntUnion2:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> IntUnion2:
        return cls.from_json_dict(json.loads(json_str))
    def to_json_dict(self):
        return self.int_union2.to_json_dict()
    @classmethod
    def from_json_dict(cls, json_value) -> IntUnion2:
        return cls(IntUnion.from_json_dict(json_value))
    def __hash__(self):
        return hash((self.int_union2,))
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.int_union2 == other.int_union2
    def __repr__(self):
        return f"<IntUnion2 [int_union2={self.int_union2}]>"
