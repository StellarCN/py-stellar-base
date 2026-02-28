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

__all__ = ['Error']
class Error:
    """
    XDR Source Code::

        typedef int Error;
    """
    def __init__(self, error: int) -> None:
        self.error = error
    def pack(self, packer: Packer) -> None:
        Integer(self.error).pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH) -> Error:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        error = Integer.unpack(unpacker)
        return cls(error)
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Error:
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
    def from_xdr(cls, xdr: str) -> Error:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Error:
        return cls.from_json_dict(json.loads(json_str))
    def to_json_dict(self):
        return Integer.to_json_dict(self.error)
    @classmethod
    def from_json_dict(cls, json_value) -> Error:
        return cls(Integer.from_json_dict(json_value))
    def __hash__(self):
        return hash((self.error,))
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.error == other.error
    def __repr__(self):
        return f"<Error [error={self.error}]>"
