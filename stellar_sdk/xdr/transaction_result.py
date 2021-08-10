# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .int64 import Int64
from .transaction_result_ext import TransactionResultExt
from .transaction_result_result import TransactionResultResult

__all__ = ["TransactionResult"]


class TransactionResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct TransactionResult
    {
        int64 feeCharged; // actual fee charged for the transaction

        union switch (TransactionResultCode code)
        {
        case txFEE_BUMP_INNER_SUCCESS:
        case txFEE_BUMP_INNER_FAILED:
            InnerTransactionResultPair innerResultPair;
        case txSUCCESS:
        case txFAILED:
            OperationResult results<>;
        default:
            void;
        }
        result;

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
        fee_charged: Int64,
        result: TransactionResultResult,
        ext: TransactionResultExt,
    ) -> None:
        self.fee_charged = fee_charged
        self.result = result
        self.ext = ext

    def pack(self, packer: Packer) -> None:
        self.fee_charged.pack(packer)
        self.result.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionResult":
        fee_charged = Int64.unpack(unpacker)
        result = TransactionResultResult.unpack(unpacker)
        ext = TransactionResultExt.unpack(unpacker)
        return cls(
            fee_charged=fee_charged,
            result=result,
            ext=ext,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "TransactionResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionResult":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.fee_charged == other.fee_charged
            and self.result == other.result
            and self.ext == other.ext
        )

    def __str__(self):
        out = [
            f"fee_charged={self.fee_charged}",
            f"result={self.result}",
            f"ext={self.ext}",
        ]
        return f"<TransactionResult {[', '.join(out)]}>"
