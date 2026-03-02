# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .transaction_history_entry_ext import TransactionHistoryEntryExt
from .transaction_set import TransactionSet
from .uint32 import Uint32

__all__ = ["TransactionHistoryEntry"]


class TransactionHistoryEntry:
    """
    XDR Source Code::

        struct TransactionHistoryEntry
        {
            uint32 ledgerSeq;
            TransactionSet txSet;

            // when v != 0, txSet must be empty
            union switch (int v)
            {
            case 0:
                void;
            case 1:
                GeneralizedTransactionSet generalizedTxSet;
            }
            ext;
        };
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> TransactionHistoryEntry:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        ledger_seq = Uint32.unpack(unpacker, depth_limit - 1)
        tx_set = TransactionSet.unpack(unpacker, depth_limit - 1)
        ext = TransactionHistoryEntryExt.unpack(unpacker, depth_limit - 1)
        return cls(
            ledger_seq=ledger_seq,
            tx_set=tx_set,
            ext=ext,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TransactionHistoryEntry:
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
    def from_xdr(cls, xdr: str) -> TransactionHistoryEntry:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TransactionHistoryEntry:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "ledger_seq": self.ledger_seq.to_json_dict(),
            "tx_set": self.tx_set.to_json_dict(),
            "ext": self.ext.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> TransactionHistoryEntry:
        ledger_seq = Uint32.from_json_dict(json_dict["ledger_seq"])
        tx_set = TransactionSet.from_json_dict(json_dict["tx_set"])
        ext = TransactionHistoryEntryExt.from_json_dict(json_dict["ext"])
        return cls(
            ledger_seq=ledger_seq,
            tx_set=tx_set,
            ext=ext,
        )

    def __hash__(self):
        return hash(
            (
                self.ledger_seq,
                self.tx_set,
                self.ext,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ledger_seq == other.ledger_seq
            and self.tx_set == other.tx_set
            and self.ext == other.ext
        )

    def __repr__(self):
        out = [
            f"ledger_seq={self.ledger_seq}",
            f"tx_set={self.tx_set}",
            f"ext={self.ext}",
        ]
        return f"<TransactionHistoryEntry [{', '.join(out)}]>"
