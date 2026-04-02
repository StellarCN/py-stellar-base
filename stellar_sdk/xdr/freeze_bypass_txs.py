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
__all__ = ['FreezeBypassTxs']
class FreezeBypassTxs:
    """
    XDR Source Code::

        struct FreezeBypassTxs {
            Hash txHashes<>;
        };
    """
    def __init__(
        self,
        tx_hashes: List[Hash],
    ) -> None:
        _expect_max_length = 4294967295
        if tx_hashes and len(tx_hashes) > _expect_max_length:
            raise ValueError(f"The maximum length of `tx_hashes` should be {_expect_max_length}, but got {len(tx_hashes)}.")
        self.tx_hashes = tx_hashes
    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.tx_hashes))
        for tx_hashes_item in self.tx_hashes:
            tx_hashes_item.pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH) -> FreezeBypassTxs:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(f"tx_hashes length {length} exceeds remaining input length {_remaining}")
        tx_hashes = []
        for _ in range(length):
            tx_hashes.append(Hash.unpack(unpacker, depth_limit - 1))
        return cls(
            tx_hashes=tx_hashes,
        )
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> FreezeBypassTxs:
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
    def from_xdr(cls, xdr: str) -> FreezeBypassTxs:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> FreezeBypassTxs:
        return cls.from_json_dict(json.loads(json_str))
    def to_json_dict(self) -> dict:
        return {
            "tx_hashes": [item.to_json_dict() for item in self.tx_hashes],
        }
    @classmethod
    def from_json_dict(cls, json_dict: dict) -> FreezeBypassTxs:
        tx_hashes = [Hash.from_json_dict(item) for item in json_dict["tx_hashes"]]
        return cls(
            tx_hashes=tx_hashes,
        )
    def __hash__(self):
        return hash((self.tx_hashes,))
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.tx_hashes == other.tx_hashes
    def __repr__(self):
        out = [
            f'tx_hashes={self.tx_hashes}',
        ]
        return f"<FreezeBypassTxs [{', '.join(out)}]>"
