# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .transaction_history_entry_ext import TransactionHistoryEntryExt
from .transaction_set import TransactionSet
from .uint32 import Uint32

__all__ = ["TransactionHistoryEntry"]


class TransactionHistoryEntry:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct TransactionHistoryEntry
    {
        uint32 ledgerSeq;
        TransactionSet txSet;
    
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
        self,
        ledger_seq: Uint32,
        tx_set: TransactionSet,
        ext: TransactionHistoryEntryExt,
    ) -> None:
        self.ledger_seq = ledger_seq
        self.tx_set = tx_set
        self.ext = ext

    def pack(self, packer: Packer) -> None:
        self.ledger_seq.pack(packer)
        self.tx_set.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionHistoryEntry":
        ledger_seq = Uint32.unpack(unpacker)
        tx_set = TransactionSet.unpack(unpacker)
        ext = TransactionHistoryEntryExt.unpack(unpacker)
        return cls(ledger_seq=ledger_seq, tx_set=tx_set, ext=ext,)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "TransactionHistoryEntry":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionHistoryEntry":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ledger_seq == other.ledger_seq
            and self.tx_set == other.tx_set
            and self.ext == other.ext
        )

    def __str__(self):
        out = [
            f"ledger_seq={self.ledger_seq}",
            f"tx_set={self.tx_set}",
            f"ext={self.ext}",
        ]
        return f"<TransactionHistoryEntry {[', '.join(out)]}>"
