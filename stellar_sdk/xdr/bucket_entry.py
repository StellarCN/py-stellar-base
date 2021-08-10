# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from ..exceptions import ValueError
from .bucket_entry_type import BucketEntryType
from .bucket_metadata import BucketMetadata
from .ledger_entry import LedgerEntry
from .ledger_key import LedgerKey

__all__ = ["BucketEntry"]


class BucketEntry:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union BucketEntry switch (BucketEntryType type)
    {
    case LIVEENTRY:
    case INITENTRY:
        LedgerEntry liveEntry;

    case DEADENTRY:
        LedgerKey deadEntry;
    case METAENTRY:
        BucketMetadata metaEntry;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: BucketEntryType,
        live_entry: LedgerEntry = None,
        dead_entry: LedgerKey = None,
        meta_entry: BucketMetadata = None,
    ) -> None:
        self.type = type
        self.live_entry = live_entry
        self.dead_entry = dead_entry
        self.meta_entry = meta_entry

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if (
            self.type == BucketEntryType.LIVEENTRY
            or self.type == BucketEntryType.INITENTRY
        ):
            if self.live_entry is None:
                raise ValueError("live_entry should not be None.")
            self.live_entry.pack(packer)
            return
        if self.type == BucketEntryType.DEADENTRY:
            if self.dead_entry is None:
                raise ValueError("dead_entry should not be None.")
            self.dead_entry.pack(packer)
            return
        if self.type == BucketEntryType.METAENTRY:
            if self.meta_entry is None:
                raise ValueError("meta_entry should not be None.")
            self.meta_entry.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "BucketEntry":
        type = BucketEntryType.unpack(unpacker)
        if type == BucketEntryType.LIVEENTRY or type == BucketEntryType.INITENTRY:
            live_entry = LedgerEntry.unpack(unpacker)
            if live_entry is None:
                raise ValueError("live_entry should not be None.")
            return cls(type, live_entry=live_entry)
        if type == BucketEntryType.DEADENTRY:
            dead_entry = LedgerKey.unpack(unpacker)
            if dead_entry is None:
                raise ValueError("dead_entry should not be None.")
            return cls(type, dead_entry=dead_entry)
        if type == BucketEntryType.METAENTRY:
            meta_entry = BucketMetadata.unpack(unpacker)
            if meta_entry is None:
                raise ValueError("meta_entry should not be None.")
            return cls(type, meta_entry=meta_entry)
        return cls(type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "BucketEntry":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "BucketEntry":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.live_entry == other.live_entry
            and self.dead_entry == other.dead_entry
            and self.meta_entry == other.meta_entry
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(
            f"live_entry={self.live_entry}"
        ) if self.live_entry is not None else None
        out.append(
            f"dead_entry={self.dead_entry}"
        ) if self.dead_entry is not None else None
        out.append(
            f"meta_entry={self.meta_entry}"
        ) if self.meta_entry is not None else None
        return f"<BucketEntry {[', '.join(out)]}>"
