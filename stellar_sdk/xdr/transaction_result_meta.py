# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .ledger_entry_changes import LedgerEntryChanges
from .transaction_meta import TransactionMeta
from .transaction_result_pair import TransactionResultPair

__all__ = ["TransactionResultMeta"]


class TransactionResultMeta:
    """
    XDR Source Code::

        struct TransactionResultMeta
        {
            TransactionResultPair result;
            LedgerEntryChanges feeProcessing;
            TransactionMeta txApplyProcessing;
        };
    """

    def __init__(
        self,
        result: TransactionResultPair,
        fee_processing: LedgerEntryChanges,
        tx_apply_processing: TransactionMeta,
    ) -> None:
        self.result = result
        self.fee_processing = fee_processing
        self.tx_apply_processing = tx_apply_processing

    def pack(self, packer: Packer) -> None:
        self.result.pack(packer)
        self.fee_processing.pack(packer)
        self.tx_apply_processing.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> TransactionResultMeta:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        result = TransactionResultPair.unpack(unpacker, depth_limit - 1)
        fee_processing = LedgerEntryChanges.unpack(unpacker, depth_limit - 1)
        tx_apply_processing = TransactionMeta.unpack(unpacker, depth_limit - 1)
        return cls(
            result=result,
            fee_processing=fee_processing,
            tx_apply_processing=tx_apply_processing,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TransactionResultMeta:
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
    def from_xdr(cls, xdr: str) -> TransactionResultMeta:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TransactionResultMeta:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "result": self.result.to_json_dict(),
            "fee_processing": self.fee_processing.to_json_dict(),
            "tx_apply_processing": self.tx_apply_processing.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> TransactionResultMeta:
        result = TransactionResultPair.from_json_dict(json_dict["result"])
        fee_processing = LedgerEntryChanges.from_json_dict(json_dict["fee_processing"])
        tx_apply_processing = TransactionMeta.from_json_dict(
            json_dict["tx_apply_processing"]
        )
        return cls(
            result=result,
            fee_processing=fee_processing,
            tx_apply_processing=tx_apply_processing,
        )

    def __hash__(self):
        return hash(
            (
                self.result,
                self.fee_processing,
                self.tx_apply_processing,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.result == other.result
            and self.fee_processing == other.fee_processing
            and self.tx_apply_processing == other.tx_apply_processing
        )

    def __repr__(self):
        out = [
            f"result={self.result}",
            f"fee_processing={self.fee_processing}",
            f"tx_apply_processing={self.tx_apply_processing}",
        ]
        return f"<TransactionResultMeta [{', '.join(out)}]>"
