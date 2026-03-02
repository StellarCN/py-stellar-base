# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_HOT_ARCHIVE_BUCKET_ENTRY_TYPE_MAP = {-1: "metaentry", 0: "archived", 1: "live"}
_HOT_ARCHIVE_BUCKET_ENTRY_TYPE_REVERSE_MAP = {"metaentry": -1, "archived": 0, "live": 1}
__all__ = ["HotArchiveBucketEntryType"]


class HotArchiveBucketEntryType(IntEnum):
    """
    XDR Source Code::

        enum HotArchiveBucketEntryType
        {
            HOT_ARCHIVE_METAENTRY = -1, // Bucket metadata, should come first.
            HOT_ARCHIVE_ARCHIVED = 0,   // Entry is Archived
            HOT_ARCHIVE_LIVE = 1        // Entry was previously HOT_ARCHIVE_ARCHIVED, but
                                        // has been added back to the live BucketList.
                                        // Does not need to be persisted.
        };
    """

    HOT_ARCHIVE_METAENTRY = -1
    HOT_ARCHIVE_ARCHIVED = 0
    HOT_ARCHIVE_LIVE = 1

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> HotArchiveBucketEntryType:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> HotArchiveBucketEntryType:
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
    def from_xdr(cls, xdr: str) -> HotArchiveBucketEntryType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> HotArchiveBucketEntryType:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _HOT_ARCHIVE_BUCKET_ENTRY_TYPE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> HotArchiveBucketEntryType:
        return cls(_HOT_ARCHIVE_BUCKET_ENTRY_TYPE_REVERSE_MAP[json_value])
