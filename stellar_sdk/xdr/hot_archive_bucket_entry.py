# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .bucket_metadata import BucketMetadata
from .hot_archive_bucket_entry_type import HotArchiveBucketEntryType
from .ledger_entry import LedgerEntry
from .ledger_key import LedgerKey

__all__ = ["HotArchiveBucketEntry"]


class HotArchiveBucketEntry:
    """
    XDR Source Code::

        union HotArchiveBucketEntry switch (HotArchiveBucketEntryType type)
        {
        case HOT_ARCHIVE_ARCHIVED:
            LedgerEntry archivedEntry;

        case HOT_ARCHIVE_LIVE:
            LedgerKey key;
        case HOT_ARCHIVE_METAENTRY:
            BucketMetadata metaEntry;
        };
    """

    def __init__(
        self,
        type: HotArchiveBucketEntryType,
        archived_entry: Optional[LedgerEntry] = None,
        key: Optional[LedgerKey] = None,
        meta_entry: Optional[BucketMetadata] = None,
    ) -> None:
        self.type = type
        self.archived_entry = archived_entry
        self.key = key
        self.meta_entry = meta_entry

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == HotArchiveBucketEntryType.HOT_ARCHIVE_ARCHIVED:
            if self.archived_entry is None:
                raise ValueError("archived_entry should not be None.")
            self.archived_entry.pack(packer)
            return
        if self.type == HotArchiveBucketEntryType.HOT_ARCHIVE_LIVE:
            if self.key is None:
                raise ValueError("key should not be None.")
            self.key.pack(packer)
            return
        if self.type == HotArchiveBucketEntryType.HOT_ARCHIVE_METAENTRY:
            if self.meta_entry is None:
                raise ValueError("meta_entry should not be None.")
            self.meta_entry.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> HotArchiveBucketEntry:
        type = HotArchiveBucketEntryType.unpack(unpacker)
        if type == HotArchiveBucketEntryType.HOT_ARCHIVE_ARCHIVED:
            archived_entry = LedgerEntry.unpack(unpacker)
            return cls(type=type, archived_entry=archived_entry)
        if type == HotArchiveBucketEntryType.HOT_ARCHIVE_LIVE:
            key = LedgerKey.unpack(unpacker)
            return cls(type=type, key=key)
        if type == HotArchiveBucketEntryType.HOT_ARCHIVE_METAENTRY:
            meta_entry = BucketMetadata.unpack(unpacker)
            return cls(type=type, meta_entry=meta_entry)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> HotArchiveBucketEntry:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> HotArchiveBucketEntry:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.type,
                self.archived_entry,
                self.key,
                self.meta_entry,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.archived_entry == other.archived_entry
            and self.key == other.key
            and self.meta_entry == other.meta_entry
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        (
            out.append(f"archived_entry={self.archived_entry}")
            if self.archived_entry is not None
            else None
        )
        out.append(f"key={self.key}") if self.key is not None else None
        (
            out.append(f"meta_entry={self.meta_entry}")
            if self.meta_entry is not None
            else None
        )
        return f"<HotArchiveBucketEntry [{', '.join(out)}]>"
