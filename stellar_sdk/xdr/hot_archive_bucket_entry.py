# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> HotArchiveBucketEntry:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = HotArchiveBucketEntryType.unpack(unpacker)
        if type == HotArchiveBucketEntryType.HOT_ARCHIVE_ARCHIVED:
            archived_entry = LedgerEntry.unpack(unpacker, depth_limit - 1)
            return cls(type=type, archived_entry=archived_entry)
        if type == HotArchiveBucketEntryType.HOT_ARCHIVE_LIVE:
            key = LedgerKey.unpack(unpacker, depth_limit - 1)
            return cls(type=type, key=key)
        if type == HotArchiveBucketEntryType.HOT_ARCHIVE_METAENTRY:
            meta_entry = BucketMetadata.unpack(unpacker, depth_limit - 1)
            return cls(type=type, meta_entry=meta_entry)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> HotArchiveBucketEntry:
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
    def from_xdr(cls, xdr: str) -> HotArchiveBucketEntry:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> HotArchiveBucketEntry:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.type == HotArchiveBucketEntryType.HOT_ARCHIVE_ARCHIVED:
            assert self.archived_entry is not None
            return {"archived": self.archived_entry.to_json_dict()}
        if self.type == HotArchiveBucketEntryType.HOT_ARCHIVE_LIVE:
            assert self.key is not None
            return {"live": self.key.to_json_dict()}
        if self.type == HotArchiveBucketEntryType.HOT_ARCHIVE_METAENTRY:
            assert self.meta_entry is not None
            return {"metaentry": self.meta_entry.to_json_dict()}
        raise ValueError(f"Unknown type in HotArchiveBucketEntry: {self.type}")

    @classmethod
    def from_json_dict(cls, json_value: dict) -> HotArchiveBucketEntry:
        if len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for HotArchiveBucketEntry, got: {json_value}"
            )
        key = next(iter(json_value))
        type = HotArchiveBucketEntryType.from_json_dict(key)
        if key == "archived":
            archived_entry = LedgerEntry.from_json_dict(json_value["archived"])
            return cls(type=type, archived_entry=archived_entry)
        if key == "live":
            key = LedgerKey.from_json_dict(json_value["live"])
            return cls(type=type, key=key)
        if key == "metaentry":
            meta_entry = BucketMetadata.from_json_dict(json_value["metaentry"])
            return cls(type=type, meta_entry=meta_entry)
        raise ValueError(f"Unknown key '{key}' for HotArchiveBucketEntry")

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
        if self.archived_entry is not None:
            out.append(f"archived_entry={self.archived_entry}")
        if self.key is not None:
            out.append(f"key={self.key}")
        if self.meta_entry is not None:
            out.append(f"meta_entry={self.meta_entry}")
        return f"<HotArchiveBucketEntry [{', '.join(out)}]>"
