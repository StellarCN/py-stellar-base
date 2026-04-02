# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .encoded_ledger_key import EncodedLedgerKey

__all__ = ["FrozenLedgerKeys"]


class FrozenLedgerKeys:
    """
    XDR Source Code::

        struct FrozenLedgerKeys {
            EncodedLedgerKey keys<>;
        };
    """

    def __init__(
        self,
        keys: List[EncodedLedgerKey],
    ) -> None:
        _expect_max_length = 4294967295
        if keys and len(keys) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `keys` should be {_expect_max_length}, but got {len(keys)}."
            )
        self.keys = keys

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.keys))
        for keys_item in self.keys:
            keys_item.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> FrozenLedgerKeys:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"keys length {length} exceeds remaining input length {_remaining}"
            )
        keys = []
        for _ in range(length):
            keys.append(EncodedLedgerKey.unpack(unpacker, depth_limit - 1))
        return cls(
            keys=keys,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> FrozenLedgerKeys:
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
    def from_xdr(cls, xdr: str) -> FrozenLedgerKeys:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> FrozenLedgerKeys:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "keys": [item.to_json_dict() for item in self.keys],
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> FrozenLedgerKeys:
        keys = [EncodedLedgerKey.from_json_dict(item) for item in json_dict["keys"]]
        return cls(
            keys=keys,
        )

    def __hash__(self):
        return hash((self.keys,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.keys == other.keys

    def __repr__(self):
        out = [
            f"keys={self.keys}",
        ]
        return f"<FrozenLedgerKeys [{', '.join(out)}]>"
