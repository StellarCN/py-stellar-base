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
__all__ = ['OptHash2']
class OptHash2:
    """
    XDR Source Code::

        typedef Hash* optHash2;
    """
    def __init__(self, opt_hash2: Optional[Hash]) -> None:
        self.opt_hash2 = opt_hash2
    def pack(self, packer: Packer) -> None:
        if self.opt_hash2 is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.opt_hash2.pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH) -> OptHash2:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        opt_hash2 = Hash.unpack(unpacker, depth_limit - 1) if unpacker.unpack_uint() else None
        return cls(opt_hash2)
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> OptHash2:
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
    def from_xdr(cls, xdr: str) -> OptHash2:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> OptHash2:
        return cls.from_json_dict(json.loads(json_str))
    def to_json_dict(self):
        return self.opt_hash2.to_json_dict() if self.opt_hash2 is not None else None
    @classmethod
    def from_json_dict(cls, json_value: str | None) -> OptHash2:
        return cls(Hash.from_json_dict(json_value) if json_value is not None else None)
    def __hash__(self):
        return hash((self.opt_hash2,))
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.opt_hash2 == other.opt_hash2
    def __repr__(self):
        return f"<OptHash2 [opt_hash2={self.opt_hash2}]>"
