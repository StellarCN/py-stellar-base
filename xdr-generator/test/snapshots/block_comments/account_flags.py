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

_ACCOUNT_FLAGS_MAP = {1: "auth_required_flag"}
_ACCOUNT_FLAGS_REVERSE_MAP = {"auth_required_flag": 1}
__all__ = ['AccountFlags']
class AccountFlags(IntEnum):
    """
    XDR Source Code::

        enum AccountFlags
        { // masks for each flag
            AUTH_REQUIRED_FLAG = 0x1
        };
    """
    AUTH_REQUIRED_FLAG = 1
    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> AccountFlags:
        value = unpacker.unpack_int()
        return cls(value)
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> AccountFlags:
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
    def from_xdr(cls, xdr: str) -> AccountFlags:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> AccountFlags:
        return cls.from_json_dict(json.loads(json_str))
    def to_json_dict(self) -> str:
        return _ACCOUNT_FLAGS_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> AccountFlags:
        return cls(_ACCOUNT_FLAGS_REVERSE_MAP[json_value])
