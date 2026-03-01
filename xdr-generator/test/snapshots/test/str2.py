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

__all__ = ['Str2']
class Str2:
    """
    XDR Source Code::

        typedef string str2<>;
    """
    def __init__(self, str2: bytes) -> None:
        _expect_max_length = 4294967295
        if str2 and len(str2) > _expect_max_length:
            raise ValueError(f"The maximum length of `str2` should be {_expect_max_length}, but got {len(str2)}.")
        self.str2 = str2
    def pack(self, packer: Packer) -> None:
        String(self.str2, 4294967295).pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH) -> Str2:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        str2 = String.unpack(unpacker, 4294967295)
        return cls(str2)
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Str2:
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
    def from_xdr(cls, xdr: str) -> Str2:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Str2:
        return cls.from_json_dict(json.loads(json_str))
    def to_json_dict(self):
        return String.to_json_dict(self.str2)
    @classmethod
    def from_json_dict(cls, json_value: str) -> Str2:
        return cls(String.from_json_dict(json_value))
    def __hash__(self):
        return hash((self.str2,))
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.str2 == other.str2
    def __repr__(self):
        return f"<Str2 [str2={self.str2}]>"
