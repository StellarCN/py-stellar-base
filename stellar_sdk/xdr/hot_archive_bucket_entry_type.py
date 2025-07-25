# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

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
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> HotArchiveBucketEntryType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
