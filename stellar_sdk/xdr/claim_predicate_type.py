# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_CLAIM_PREDICATE_TYPE_MAP = {
    0: "unconditional",
    1: "and",
    2: "or",
    3: "not",
    4: "before_absolute_time",
    5: "before_relative_time",
}
_CLAIM_PREDICATE_TYPE_REVERSE_MAP = {
    "unconditional": 0,
    "and": 1,
    "or": 2,
    "not": 3,
    "before_absolute_time": 4,
    "before_relative_time": 5,
}
__all__ = ["ClaimPredicateType"]


class ClaimPredicateType(IntEnum):
    """
    XDR Source Code::

        enum ClaimPredicateType
        {
            CLAIM_PREDICATE_UNCONDITIONAL = 0,
            CLAIM_PREDICATE_AND = 1,
            CLAIM_PREDICATE_OR = 2,
            CLAIM_PREDICATE_NOT = 3,
            CLAIM_PREDICATE_BEFORE_ABSOLUTE_TIME = 4,
            CLAIM_PREDICATE_BEFORE_RELATIVE_TIME = 5
        };
    """

    CLAIM_PREDICATE_UNCONDITIONAL = 0
    CLAIM_PREDICATE_AND = 1
    CLAIM_PREDICATE_OR = 2
    CLAIM_PREDICATE_NOT = 3
    CLAIM_PREDICATE_BEFORE_ABSOLUTE_TIME = 4
    CLAIM_PREDICATE_BEFORE_RELATIVE_TIME = 5

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ClaimPredicateType:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ClaimPredicateType:
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
    def from_xdr(cls, xdr: str) -> ClaimPredicateType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ClaimPredicateType:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _CLAIM_PREDICATE_TYPE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> ClaimPredicateType:
        return cls(_CLAIM_PREDICATE_TYPE_REVERSE_MAP[json_value])
