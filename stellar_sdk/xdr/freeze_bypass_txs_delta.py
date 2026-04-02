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
__all__ = ['FreezeBypassTxsDelta']
class FreezeBypassTxsDelta:
    """
    XDR Source Code::

        struct FreezeBypassTxsDelta {
            Hash addTxs<>;
            Hash removeTxs<>;
        };
    """
    def __init__(
        self,
        add_txs: List[Hash],
        remove_txs: List[Hash],
    ) -> None:
        _expect_max_length = 4294967295
        if add_txs and len(add_txs) > _expect_max_length:
            raise ValueError(f"The maximum length of `add_txs` should be {_expect_max_length}, but got {len(add_txs)}.")
        _expect_max_length = 4294967295
        if remove_txs and len(remove_txs) > _expect_max_length:
            raise ValueError(f"The maximum length of `remove_txs` should be {_expect_max_length}, but got {len(remove_txs)}.")
        self.add_txs = add_txs
        self.remove_txs = remove_txs
    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.add_txs))
        for add_txs_item in self.add_txs:
            add_txs_item.pack(packer)
        packer.pack_uint(len(self.remove_txs))
        for remove_txs_item in self.remove_txs:
            remove_txs_item.pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH) -> FreezeBypassTxsDelta:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(f"add_txs length {length} exceeds remaining input length {_remaining}")
        add_txs = []
        for _ in range(length):
            add_txs.append(Hash.unpack(unpacker, depth_limit - 1))
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(f"remove_txs length {length} exceeds remaining input length {_remaining}")
        remove_txs = []
        for _ in range(length):
            remove_txs.append(Hash.unpack(unpacker, depth_limit - 1))
        return cls(
            add_txs=add_txs,
            remove_txs=remove_txs,
        )
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> FreezeBypassTxsDelta:
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
    def from_xdr(cls, xdr: str) -> FreezeBypassTxsDelta:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> FreezeBypassTxsDelta:
        return cls.from_json_dict(json.loads(json_str))
    def to_json_dict(self) -> dict:
        return {
            "add_txs": [item.to_json_dict() for item in self.add_txs],
            "remove_txs": [item.to_json_dict() for item in self.remove_txs],
        }
    @classmethod
    def from_json_dict(cls, json_dict: dict) -> FreezeBypassTxsDelta:
        add_txs = [Hash.from_json_dict(item) for item in json_dict["add_txs"]]
        remove_txs = [Hash.from_json_dict(item) for item in json_dict["remove_txs"]]
        return cls(
            add_txs=add_txs,
            remove_txs=remove_txs,
        )
    def __hash__(self):
        return hash((self.add_txs, self.remove_txs,))
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.add_txs == other.add_txs and self.remove_txs == other.remove_txs
    def __repr__(self):
        out = [
            f'add_txs={self.add_txs}',
            f'remove_txs={self.remove_txs}',
        ]
        return f"<FreezeBypassTxsDelta [{', '.join(out)}]>"
