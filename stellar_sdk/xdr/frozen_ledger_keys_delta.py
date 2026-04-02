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

from .encoded_ledger_key import EncodedLedgerKey
__all__ = ['FrozenLedgerKeysDelta']
class FrozenLedgerKeysDelta:
    """
    XDR Source Code::

        struct FrozenLedgerKeysDelta {
            EncodedLedgerKey keysToFreeze<>;
            EncodedLedgerKey keysToUnfreeze<>;
        };
    """
    def __init__(
        self,
        keys_to_freeze: List[EncodedLedgerKey],
        keys_to_unfreeze: List[EncodedLedgerKey],
    ) -> None:
        _expect_max_length = 4294967295
        if keys_to_freeze and len(keys_to_freeze) > _expect_max_length:
            raise ValueError(f"The maximum length of `keys_to_freeze` should be {_expect_max_length}, but got {len(keys_to_freeze)}.")
        _expect_max_length = 4294967295
        if keys_to_unfreeze and len(keys_to_unfreeze) > _expect_max_length:
            raise ValueError(f"The maximum length of `keys_to_unfreeze` should be {_expect_max_length}, but got {len(keys_to_unfreeze)}.")
        self.keys_to_freeze = keys_to_freeze
        self.keys_to_unfreeze = keys_to_unfreeze
    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.keys_to_freeze))
        for keys_to_freeze_item in self.keys_to_freeze:
            keys_to_freeze_item.pack(packer)
        packer.pack_uint(len(self.keys_to_unfreeze))
        for keys_to_unfreeze_item in self.keys_to_unfreeze:
            keys_to_unfreeze_item.pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH) -> FrozenLedgerKeysDelta:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(f"keys_to_freeze length {length} exceeds remaining input length {_remaining}")
        keys_to_freeze = []
        for _ in range(length):
            keys_to_freeze.append(EncodedLedgerKey.unpack(unpacker, depth_limit - 1))
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(f"keys_to_unfreeze length {length} exceeds remaining input length {_remaining}")
        keys_to_unfreeze = []
        for _ in range(length):
            keys_to_unfreeze.append(EncodedLedgerKey.unpack(unpacker, depth_limit - 1))
        return cls(
            keys_to_freeze=keys_to_freeze,
            keys_to_unfreeze=keys_to_unfreeze,
        )
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> FrozenLedgerKeysDelta:
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
    def from_xdr(cls, xdr: str) -> FrozenLedgerKeysDelta:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> FrozenLedgerKeysDelta:
        return cls.from_json_dict(json.loads(json_str))
    def to_json_dict(self) -> dict:
        return {
            "keys_to_freeze": [item.to_json_dict() for item in self.keys_to_freeze],
            "keys_to_unfreeze": [item.to_json_dict() for item in self.keys_to_unfreeze],
        }
    @classmethod
    def from_json_dict(cls, json_dict: dict) -> FrozenLedgerKeysDelta:
        keys_to_freeze = [EncodedLedgerKey.from_json_dict(item) for item in json_dict["keys_to_freeze"]]
        keys_to_unfreeze = [EncodedLedgerKey.from_json_dict(item) for item in json_dict["keys_to_unfreeze"]]
        return cls(
            keys_to_freeze=keys_to_freeze,
            keys_to_unfreeze=keys_to_unfreeze,
        )
    def __hash__(self):
        return hash((self.keys_to_freeze, self.keys_to_unfreeze,))
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.keys_to_freeze == other.keys_to_freeze and self.keys_to_unfreeze == other.keys_to_unfreeze
    def __repr__(self):
        out = [
            f'keys_to_freeze={self.keys_to_freeze}',
            f'keys_to_unfreeze={self.keys_to_unfreeze}',
        ]
        return f"<FrozenLedgerKeysDelta [{', '.join(out)}]>"
