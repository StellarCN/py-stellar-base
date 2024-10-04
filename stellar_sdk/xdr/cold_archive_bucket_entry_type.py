# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

__all__ = ["ColdArchiveBucketEntryType"]


class ColdArchiveBucketEntryType(IntEnum):
    """
    XDR Source Code::

        enum ColdArchiveBucketEntryType
        {
            COLD_ARCHIVE_METAENTRY     = -1,  // Bucket metadata, should come first.
            COLD_ARCHIVE_ARCHIVED_LEAF = 0,   // Full LedgerEntry that was archived during the epoch
            COLD_ARCHIVE_DELETED_LEAF  = 1,   // LedgerKey that was deleted during the epoch
            COLD_ARCHIVE_BOUNDARY_LEAF = 2,   // Dummy leaf representing low/high bound
            COLD_ARCHIVE_HASH          = 3    // Intermediary Merkle hash entry
        };
    """

    COLD_ARCHIVE_METAENTRY = -1
    COLD_ARCHIVE_ARCHIVED_LEAF = 0
    COLD_ARCHIVE_DELETED_LEAF = 1
    COLD_ARCHIVE_BOUNDARY_LEAF = 2
    COLD_ARCHIVE_HASH = 3

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ColdArchiveBucketEntryType:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ColdArchiveBucketEntryType:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ColdArchiveBucketEntryType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
