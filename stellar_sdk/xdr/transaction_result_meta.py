# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .ledger_entry_changes import LedgerEntryChanges
from .transaction_meta import TransactionMeta
from .transaction_result_pair import TransactionResultPair

__all__ = ["TransactionResultMeta"]


class TransactionResultMeta:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct TransactionResultMeta
    {
        TransactionResultPair result;
        LedgerEntryChanges feeProcessing;
        TransactionMeta txApplyProcessing;
    };
    ----------------------------------------------------------------
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
    def unpack(cls, unpacker: Unpacker) -> "TransactionResultMeta":
        result = TransactionResultPair.unpack(unpacker)
        fee_processing = LedgerEntryChanges.unpack(unpacker)
        tx_apply_processing = TransactionMeta.unpack(unpacker)
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
    def from_xdr_bytes(cls, xdr: bytes) -> "TransactionResultMeta":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionResultMeta":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.result == other.result
            and self.fee_processing == other.fee_processing
            and self.tx_apply_processing == other.tx_apply_processing
        )

    def __str__(self):
        out = [
            f"result={self.result}",
            f"fee_processing={self.fee_processing}",
            f"tx_apply_processing={self.tx_apply_processing}",
        ]
        return f"<TransactionResultMeta {[', '.join(out)]}>"
