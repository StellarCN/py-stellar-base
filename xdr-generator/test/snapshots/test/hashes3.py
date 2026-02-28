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

from .hash import Hash
__all__ = ['Hashes3']
class Hashes3:
    """
    XDR Source Code::

        typedef Hash Hashes3<>;
    """
    def __init__(self, hashes3: List[Hash]) -> None:
        _expect_max_length = 4294967295
        if hashes3 and len(hashes3) > _expect_max_length:
            raise ValueError(f"The maximum length of `hashes3` should be {_expect_max_length}, but got {len(hashes3)}.")
        self.hashes3 = hashes3
    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.hashes3))
        for hashes3_item in self.hashes3:
            hashes3_item.pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH) -> Hashes3:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(f"hashes3 length {length} exceeds remaining input length {_remaining}")
        hashes3 = []
        for _ in range(length):
            hashes3.append(Hash.unpack(unpacker, depth_limit - 1))
        return cls(hashes3)
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Hashes3:
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
    def from_xdr(cls, xdr: str) -> Hashes3:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Hashes3:
        return cls.from_json_dict(json.loads(json_str))
    def to_json_dict(self):
        return [item.to_json_dict() for item in self.hashes3]
    @classmethod
    def from_json_dict(cls, json_value) -> Hashes3:
        return cls([Hash.from_json_dict(item) for item in json_value])
    def __hash__(self):
        return hash((self.hashes3,))
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.hashes3 == other.hashes3
    def __repr__(self):
        return f"<Hashes3 [hashes3={self.hashes3}]>"
