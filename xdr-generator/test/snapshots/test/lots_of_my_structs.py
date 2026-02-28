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

from .my_struct import MyStruct
__all__ = ['LotsOfMyStructs']
class LotsOfMyStructs:
    """
    XDR Source Code::

        struct LotsOfMyStructs
        {
            MyStruct members<>;
        };
    """
    def __init__(
        self,
        members: List[MyStruct],
    ) -> None:
        _expect_max_length = 4294967295
        if members and len(members) > _expect_max_length:
            raise ValueError(f"The maximum length of `members` should be {_expect_max_length}, but got {len(members)}.")
        self.members = members
    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.members))
        for members_item in self.members:
            members_item.pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH) -> LotsOfMyStructs:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(f"members length {length} exceeds remaining input length {_remaining}")
        members = []
        for _ in range(length):
            members.append(MyStruct.unpack(unpacker, depth_limit - 1))
        return cls(
            members=members,
        )
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LotsOfMyStructs:
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
    def from_xdr(cls, xdr: str) -> LotsOfMyStructs:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LotsOfMyStructs:
        return cls.from_json_dict(json.loads(json_str))
    def to_json_dict(self) -> dict:
        return {
            "members": [item.to_json_dict() for item in self.members],
        }
    @classmethod
    def from_json_dict(cls, json_dict: dict) -> LotsOfMyStructs:
        members = [MyStruct.from_json_dict(item) for item in json_dict["members"]]
        return cls(
            members=members,
        )
    def __hash__(self):
        return hash((self.members,))
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.members == other.members
    def __repr__(self):
        out = [
            f'members={self.members}',
        ]
        return f"<LotsOfMyStructs [{', '.join(out)}]>"
