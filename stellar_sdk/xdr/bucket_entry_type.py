# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_BUCKET_ENTRY_TYPE_MAP = {
    -1: "metaentry",
    0: "liveentry",
    1: "deadentry",
    2: "initentry",
}
_BUCKET_ENTRY_TYPE_REVERSE_MAP = {
    "metaentry": -1,
    "liveentry": 0,
    "deadentry": 1,
    "initentry": 2,
}
__all__ = ["BucketEntryType"]


class BucketEntryType(IntEnum):
    """
    XDR Source Code::

        enum BucketEntryType
        {
            METAENTRY =
                -1, // At-and-after protocol 11: bucket metadata, should come first.
            LIVEENTRY = 0, // Before protocol 11: created-or-updated;
                           // At-and-after protocol 11: only updated.
            DEADENTRY = 1,
            INITENTRY = 2 // At-and-after protocol 11: only created.
        };
    """

    METAENTRY = -1
    LIVEENTRY = 0
    DEADENTRY = 1
    INITENTRY = 2

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> BucketEntryType:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> BucketEntryType:
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
    def from_xdr(cls, xdr: str) -> BucketEntryType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> BucketEntryType:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _BUCKET_ENTRY_TYPE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> BucketEntryType:
        return cls(_BUCKET_ENTRY_TYPE_REVERSE_MAP[json_value])
