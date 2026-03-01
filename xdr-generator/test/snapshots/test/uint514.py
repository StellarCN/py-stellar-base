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

__all__ = ['Uint514']
class Uint514:
    """
    XDR Source Code::

        typedef opaque uint514<>;
    """
    def __init__(self, uint514: bytes) -> None:
        _expect_max_length = 4294967295
        if uint514 and len(uint514) > _expect_max_length:
            raise ValueError(f"The maximum length of `uint514` should be {_expect_max_length}, but got {len(uint514)}.")
        self.uint514 = uint514
    def pack(self, packer: Packer) -> None:
        Opaque(self.uint514, 4294967295, False).pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH) -> Uint514:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        uint514 = Opaque.unpack(unpacker, 4294967295, False)
        return cls(uint514)
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Uint514:
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
    def from_xdr(cls, xdr: str) -> Uint514:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Uint514:
        return cls.from_json_dict(json.loads(json_str))
    def to_json_dict(self):
        return Opaque.to_json_dict(self.uint514)
    @classmethod
    def from_json_dict(cls, json_value: str) -> Uint514:
        return cls(Opaque.from_json_dict(json_value))
    def __hash__(self):
        return hash((self.uint514,))
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.uint514 == other.uint514
    def __repr__(self):
        return f"<Uint514 [uint514={self.uint514}]>"
