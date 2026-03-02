# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_THRESHOLD_INDEXES_MAP = {0: "master_weight", 1: "low", 2: "med", 3: "high"}
_THRESHOLD_INDEXES_REVERSE_MAP = {"master_weight": 0, "low": 1, "med": 2, "high": 3}
__all__ = ["ThresholdIndexes"]


class ThresholdIndexes(IntEnum):
    """
    XDR Source Code::

        enum ThresholdIndexes
        {
            THRESHOLD_MASTER_WEIGHT = 0,
            THRESHOLD_LOW = 1,
            THRESHOLD_MED = 2,
            THRESHOLD_HIGH = 3
        };
    """

    THRESHOLD_MASTER_WEIGHT = 0
    THRESHOLD_LOW = 1
    THRESHOLD_MED = 2
    THRESHOLD_HIGH = 3

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ThresholdIndexes:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ThresholdIndexes:
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
    def from_xdr(cls, xdr: str) -> ThresholdIndexes:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ThresholdIndexes:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _THRESHOLD_INDEXES_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> ThresholdIndexes:
        return cls(_THRESHOLD_INDEXES_REVERSE_MAP[json_value])
