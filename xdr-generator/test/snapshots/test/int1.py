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

__all__ = ['Int1']
class Int1:
    """
    XDR Source Code::

        typedef int             int1;
    """
    def __init__(self, int1: int) -> None:
        self.int1 = int1
    def pack(self, packer: Packer) -> None:
        Integer(self.int1).pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH) -> Int1:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        int1 = Integer.unpack(unpacker)
        return cls(int1)
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Int1:
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
    def from_xdr(cls, xdr: str) -> Int1:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Int1:
        return cls.from_json_dict(json.loads(json_str))
    def to_json_dict(self):
        return Integer.to_json_dict(self.int1)
    @classmethod
    def from_json_dict(cls, json_value) -> Int1:
        return cls(Integer.from_json_dict(json_value))
    def __hash__(self):
        return hash((self.int1,))
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.int1 == other.int1
    def __repr__(self):
        return f"<Int1 [int1={self.int1}]>"
