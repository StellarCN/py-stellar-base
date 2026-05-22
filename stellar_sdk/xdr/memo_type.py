# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_MEMO_TYPE_MAP = {0: "none", 1: "text", 2: "id", 3: "hash", 4: "return"}
_MEMO_TYPE_REVERSE_MAP = {"none": 0, "text": 1, "id": 2, "hash": 3, "return": 4}
__all__ = ["MemoType"]


class MemoType(IntEnum):
    """
    XDR Source Code::

        enum MemoType
        {
            MEMO_NONE = 0,
            MEMO_TEXT = 1,
            MEMO_ID = 2,
            MEMO_HASH = 3,
            MEMO_RETURN = 4
        };
    """

    MEMO_NONE = 0
    MEMO_TEXT = 1
    MEMO_ID = 2
    MEMO_HASH = 3
    MEMO_RETURN = 4

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> MemoType:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> MemoType:
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
    def from_xdr(cls, xdr: str) -> MemoType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> MemoType:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _MEMO_TYPE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> MemoType:
        return cls(_MEMO_TYPE_REVERSE_MAP[json_value])
