# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib import Packer, Unpacker

from ..exceptions import ValueError
from .inner_transaction_result_pair import InnerTransactionResultPair
from .operation_result import OperationResult
from .transaction_result_code import TransactionResultCode

__all__ = ["TransactionResultResult"]


class TransactionResultResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
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
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        code: TransactionResultCode,
        inner_result_pair: InnerTransactionResultPair = None,
        results: List[OperationResult] = None,
    ) -> None:
        if results and len(results) > 4294967295:
            raise ValueError(
                f"The maximum length of `results` should be 4294967295, but got {len(results)}."
            )
        self.code = code
        self.inner_result_pair = inner_result_pair
        self.results = results

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if (
            self.code == TransactionResultCode.txFEE_BUMP_INNER_SUCCESS
            or self.code == TransactionResultCode.txFEE_BUMP_INNER_FAILED
        ):
            if self.inner_result_pair is None:
                raise ValueError("inner_result_pair should not be None.")
            self.inner_result_pair.pack(packer)
            return
        if (
            self.code == TransactionResultCode.txSUCCESS
            or self.code == TransactionResultCode.txFAILED
        ):
            if self.results is None:
                raise ValueError("results should not be None.")
            packer.pack_uint(len(self.results))
            for result in self.results:
                result.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionResultResult":
        code = TransactionResultCode.unpack(unpacker)
        if (
            code == TransactionResultCode.txFEE_BUMP_INNER_SUCCESS
            or code == TransactionResultCode.txFEE_BUMP_INNER_FAILED
        ):
            inner_result_pair = InnerTransactionResultPair.unpack(unpacker)
            if inner_result_pair is None:
                raise ValueError("inner_result_pair should not be None.")
            return cls(code, inner_result_pair=inner_result_pair)
        if (
            code == TransactionResultCode.txSUCCESS
            or code == TransactionResultCode.txFAILED
        ):
            length = unpacker.unpack_uint()
            results = []
            for _ in range(length):
                results.append(OperationResult.unpack(unpacker))
            return cls(code, results=results)
        return cls(code)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "TransactionResultResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionResultResult":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.code == other.code
            and self.inner_result_pair == other.inner_result_pair
            and self.results == other.results
        )

    def __str__(self):
        out = []
        out.append(f"code={self.code}")
        out.append(
            f"inner_result_pair={self.inner_result_pair}"
        ) if self.inner_result_pair is not None else None
        out.append(f"results={self.results}") if self.results is not None else None
        return f"<TransactionResultResult {[', '.join(out)]}>"
