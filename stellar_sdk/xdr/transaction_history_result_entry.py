# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .transaction_history_result_entry_ext import TransactionHistoryResultEntryExt
from .transaction_result_set import TransactionResultSet
from .uint32 import Uint32

__all__ = ["TransactionHistoryResultEntry"]


class TransactionHistoryResultEntry:
    """
    XDR Source Code::

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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> TransactionHistoryResultEntry:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        ledger_seq = Uint32.unpack(unpacker, depth_limit - 1)
        tx_result_set = TransactionResultSet.unpack(unpacker, depth_limit - 1)
        ext = TransactionHistoryResultEntryExt.unpack(unpacker, depth_limit - 1)
        return cls(
            ledger_seq=ledger_seq,
            tx_result_set=tx_result_set,
            ext=ext,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TransactionHistoryResultEntry:
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
    def from_xdr(cls, xdr: str) -> TransactionHistoryResultEntry:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TransactionHistoryResultEntry:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "ledger_seq": self.ledger_seq.to_json_dict(),
            "tx_result_set": self.tx_result_set.to_json_dict(),
            "ext": self.ext.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> TransactionHistoryResultEntry:
        ledger_seq = Uint32.from_json_dict(json_dict["ledger_seq"])
        tx_result_set = TransactionResultSet.from_json_dict(json_dict["tx_result_set"])
        ext = TransactionHistoryResultEntryExt.from_json_dict(json_dict["ext"])
        return cls(
            ledger_seq=ledger_seq,
            tx_result_set=tx_result_set,
            ext=ext,
        )

    def __hash__(self):
        return hash(
            (
                self.ledger_seq,
                self.tx_result_set,
                self.ext,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ledger_seq == other.ledger_seq
            and self.tx_result_set == other.tx_result_set
            and self.ext == other.ext
        )

    def __repr__(self):
        out = [
            f"ledger_seq={self.ledger_seq}",
            f"tx_result_set={self.tx_result_set}",
            f"ext={self.ext}",
        ]
        return f"<TransactionHistoryResultEntry [{', '.join(out)}]>"
