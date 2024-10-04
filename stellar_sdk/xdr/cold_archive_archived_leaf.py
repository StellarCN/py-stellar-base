# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .ledger_entry import LedgerEntry
from .uint32 import Uint32

__all__ = ["ColdArchiveArchivedLeaf"]


class ColdArchiveArchivedLeaf:
    """
    XDR Source Code::

        struct ColdArchiveArchivedLeaf
        {
            uint32 index;
            LedgerEntry archivedEntry;
        };
    """

    def __init__(
        self,
        index: Uint32,
        archived_entry: LedgerEntry,
    ) -> None:
        self.index = index
        self.archived_entry = archived_entry

    def pack(self, packer: Packer) -> None:
        self.index.pack(packer)
        self.archived_entry.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ColdArchiveArchivedLeaf:
        index = Uint32.unpack(unpacker)
        archived_entry = LedgerEntry.unpack(unpacker)
        return cls(
            index=index,
            archived_entry=archived_entry,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ColdArchiveArchivedLeaf:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ColdArchiveArchivedLeaf:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.index,
                self.archived_entry,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.index == other.index and self.archived_entry == other.archived_entry

    def __repr__(self):
        out = [
            f"index={self.index}",
            f"archived_entry={self.archived_entry}",
        ]
        return f"<ColdArchiveArchivedLeaf [{', '.join(out)}]>"
