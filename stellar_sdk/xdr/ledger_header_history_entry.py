# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .hash import Hash
from .ledger_header import LedgerHeader
from .ledger_header_history_entry_ext import LedgerHeaderHistoryEntryExt

__all__ = ["LedgerHeaderHistoryEntry"]


class LedgerHeaderHistoryEntry:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct LedgerHeaderHistoryEntry
    {
        Hash hash;
        LedgerHeader header;
    
        // reserved for future use
        union switch (int v)
        {
        case 0:
            void;
        }
        ext;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self, hash: Hash, header: LedgerHeader, ext: LedgerHeaderHistoryEntryExt,
    ) -> None:
        self.hash = hash
        self.header = header
        self.ext = ext

    def pack(self, packer: Packer) -> None:
        self.hash.pack(packer)
        self.header.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerHeaderHistoryEntry":
        hash = Hash.unpack(unpacker)
        header = LedgerHeader.unpack(unpacker)
        ext = LedgerHeaderHistoryEntryExt.unpack(unpacker)
        return cls(hash=hash, header=header, ext=ext,)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "LedgerHeaderHistoryEntry":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerHeaderHistoryEntry":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.hash == other.hash
            and self.header == other.header
            and self.ext == other.ext
        )

    def __str__(self):
        out = [
            f"hash={self.hash}",
            f"header={self.header}",
            f"ext={self.ext}",
        ]
        return f"<LedgerHeaderHistoryEntry {[', '.join(out)]}>"
