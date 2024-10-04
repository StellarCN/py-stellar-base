# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .bucket_metadata import BucketMetadata
from .cold_archive_archived_leaf import ColdArchiveArchivedLeaf
from .cold_archive_boundary_leaf import ColdArchiveBoundaryLeaf
from .cold_archive_bucket_entry_type import ColdArchiveBucketEntryType
from .cold_archive_deleted_leaf import ColdArchiveDeletedLeaf
from .cold_archive_hash_entry import ColdArchiveHashEntry

__all__ = ["ColdArchiveBucketEntry"]


class ColdArchiveBucketEntry:
    """
    XDR Source Code::

        union ColdArchiveBucketEntry switch (ColdArchiveBucketEntryType type)
        {
        case COLD_ARCHIVE_METAENTRY:
            BucketMetadata metaEntry;
        case COLD_ARCHIVE_ARCHIVED_LEAF:
            ColdArchiveArchivedLeaf archivedLeaf;
        case COLD_ARCHIVE_DELETED_LEAF:
            ColdArchiveDeletedLeaf deletedLeaf;
        case COLD_ARCHIVE_BOUNDARY_LEAF:
            ColdArchiveBoundaryLeaf boundaryLeaf;
        case COLD_ARCHIVE_HASH:
            ColdArchiveHashEntry hashEntry;
        };
    """

    def __init__(
        self,
        type: ColdArchiveBucketEntryType,
        meta_entry: BucketMetadata = None,
        archived_leaf: ColdArchiveArchivedLeaf = None,
        deleted_leaf: ColdArchiveDeletedLeaf = None,
        boundary_leaf: ColdArchiveBoundaryLeaf = None,
        hash_entry: ColdArchiveHashEntry = None,
    ) -> None:
        self.type = type
        self.meta_entry = meta_entry
        self.archived_leaf = archived_leaf
        self.deleted_leaf = deleted_leaf
        self.boundary_leaf = boundary_leaf
        self.hash_entry = hash_entry

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == ColdArchiveBucketEntryType.COLD_ARCHIVE_METAENTRY:
            if self.meta_entry is None:
                raise ValueError("meta_entry should not be None.")
            self.meta_entry.pack(packer)
            return
        if self.type == ColdArchiveBucketEntryType.COLD_ARCHIVE_ARCHIVED_LEAF:
            if self.archived_leaf is None:
                raise ValueError("archived_leaf should not be None.")
            self.archived_leaf.pack(packer)
            return
        if self.type == ColdArchiveBucketEntryType.COLD_ARCHIVE_DELETED_LEAF:
            if self.deleted_leaf is None:
                raise ValueError("deleted_leaf should not be None.")
            self.deleted_leaf.pack(packer)
            return
        if self.type == ColdArchiveBucketEntryType.COLD_ARCHIVE_BOUNDARY_LEAF:
            if self.boundary_leaf is None:
                raise ValueError("boundary_leaf should not be None.")
            self.boundary_leaf.pack(packer)
            return
        if self.type == ColdArchiveBucketEntryType.COLD_ARCHIVE_HASH:
            if self.hash_entry is None:
                raise ValueError("hash_entry should not be None.")
            self.hash_entry.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ColdArchiveBucketEntry:
        type = ColdArchiveBucketEntryType.unpack(unpacker)
        if type == ColdArchiveBucketEntryType.COLD_ARCHIVE_METAENTRY:
            meta_entry = BucketMetadata.unpack(unpacker)
            return cls(type=type, meta_entry=meta_entry)
        if type == ColdArchiveBucketEntryType.COLD_ARCHIVE_ARCHIVED_LEAF:
            archived_leaf = ColdArchiveArchivedLeaf.unpack(unpacker)
            return cls(type=type, archived_leaf=archived_leaf)
        if type == ColdArchiveBucketEntryType.COLD_ARCHIVE_DELETED_LEAF:
            deleted_leaf = ColdArchiveDeletedLeaf.unpack(unpacker)
            return cls(type=type, deleted_leaf=deleted_leaf)
        if type == ColdArchiveBucketEntryType.COLD_ARCHIVE_BOUNDARY_LEAF:
            boundary_leaf = ColdArchiveBoundaryLeaf.unpack(unpacker)
            return cls(type=type, boundary_leaf=boundary_leaf)
        if type == ColdArchiveBucketEntryType.COLD_ARCHIVE_HASH:
            hash_entry = ColdArchiveHashEntry.unpack(unpacker)
            return cls(type=type, hash_entry=hash_entry)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ColdArchiveBucketEntry:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ColdArchiveBucketEntry:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.type,
                self.meta_entry,
                self.archived_leaf,
                self.deleted_leaf,
                self.boundary_leaf,
                self.hash_entry,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.meta_entry == other.meta_entry
            and self.archived_leaf == other.archived_leaf
            and self.deleted_leaf == other.deleted_leaf
            and self.boundary_leaf == other.boundary_leaf
            and self.hash_entry == other.hash_entry
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        (
            out.append(f"meta_entry={self.meta_entry}")
            if self.meta_entry is not None
            else None
        )
        (
            out.append(f"archived_leaf={self.archived_leaf}")
            if self.archived_leaf is not None
            else None
        )
        (
            out.append(f"deleted_leaf={self.deleted_leaf}")
            if self.deleted_leaf is not None
            else None
        )
        (
            out.append(f"boundary_leaf={self.boundary_leaf}")
            if self.boundary_leaf is not None
            else None
        )
        (
            out.append(f"hash_entry={self.hash_entry}")
            if self.hash_entry is not None
            else None
        )
        return f"<ColdArchiveBucketEntry [{', '.join(out)}]>"
