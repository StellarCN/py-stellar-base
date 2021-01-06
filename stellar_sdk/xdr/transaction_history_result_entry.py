# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .transaction_history_result_entry_ext import TransactionHistoryResultEntryExt
from .transaction_result_set import TransactionResultSet
from .uint32 import Uint32

__all__ = ["TransactionHistoryResultEntry"]


class TransactionHistoryResultEntry:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct TransactionHistoryResultEntry
    {
        uint32 ledgerSeq;
        TransactionResultSet txResultSet;
    
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
        tx_result_set: TransactionResultSet,
        ext: TransactionHistoryResultEntryExt,
    ) -> None:
        self.ledger_seq = ledger_seq
        self.tx_result_set = tx_result_set
        self.ext = ext

    def pack(self, packer: Packer) -> None:
        self.ledger_seq.pack(packer)
        self.tx_result_set.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionHistoryResultEntry":
        ledger_seq = Uint32.unpack(unpacker)
        tx_result_set = TransactionResultSet.unpack(unpacker)
        ext = TransactionHistoryResultEntryExt.unpack(unpacker)
        return cls(ledger_seq=ledger_seq, tx_result_set=tx_result_set, ext=ext,)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "TransactionHistoryResultEntry":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionHistoryResultEntry":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ledger_seq == other.ledger_seq
            and self.tx_result_set == other.tx_result_set
            and self.ext == other.ext
        )

    def __str__(self):
        out = [
            f"ledger_seq={self.ledger_seq}",
            f"tx_result_set={self.tx_result_set}",
            f"ext={self.ext}",
        ]
        return f"<TransactionHistoryResultEntry {[', '.join(out)]}>"
