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
__all__ = ['Hashes1']
class Hashes1:
    """
    XDR Source Code::

        typedef Hash Hashes1[12];
    """
    def __init__(self, hashes1: List[Hash]) -> None:
        _expect_length = 12
        if hashes1 and len(hashes1) != _expect_length:
            raise ValueError(f"The length of `hashes1` should be {_expect_length}, but got {len(hashes1)}.")
        self.hashes1 = hashes1
    def pack(self, packer: Packer) -> None:
        for hashes1_item in self.hashes1:
            hashes1_item.pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH) -> Hashes1:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        length = 12
        hashes1 = []
        for _ in range(length):
            hashes1.append(Hash.unpack(unpacker, depth_limit - 1))
        return cls(hashes1)
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Hashes1:
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
    def from_xdr(cls, xdr: str) -> Hashes1:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Hashes1:
        return cls.from_json_dict(json.loads(json_str))
    def to_json_dict(self):
        return [item.to_json_dict() for item in self.hashes1]
    @classmethod
    def from_json_dict(cls, json_value: list) -> Hashes1:
        return cls([Hash.from_json_dict(item) for item in json_value])
    def __hash__(self):
        return hash((self.hashes1,))
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.hashes1 == other.hashes1
    def __repr__(self):
        return f"<Hashes1 [hashes1={self.hashes1}]>"
