# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib import Packer, Unpacker

from .operation_result import OperationResult
from .transaction_result_code import TransactionResultCode
from ..exceptions import ValueError

__all__ = ["InnerTransactionResultResult"]


class InnerTransactionResultResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (TransactionResultCode code)
        {
        // txFEE_BUMP_INNER_SUCCESS is not included
        case txSUCCESS:
        case txFAILED:
            OperationResult results<>;
        case txTOO_EARLY:
        case txTOO_LATE:
        case txMISSING_OPERATION:
        case txBAD_SEQ:
        case txBAD_AUTH:
        case txINSUFFICIENT_BALANCE:
        case txNO_ACCOUNT:
        case txINSUFFICIENT_FEE:
        case txBAD_AUTH_EXTRA:
        case txINTERNAL_ERROR:
        case txNOT_SUPPORTED:
        // txFEE_BUMP_INNER_FAILED is not included
        case txBAD_SPONSORSHIP:
            void;
        }
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        code: TransactionResultCode,
        results: List[OperationResult] = None,
    ) -> None:
        if results and len(results) > 4294967295:
            raise ValueError(
                f"The maximum length of `results` should be 4294967295, but got {len(results)}."
            )
        self.code = code
        self.results = results

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
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
        if (
            self.code == TransactionResultCode.txTOO_EARLY
            or self.code == TransactionResultCode.txTOO_LATE
            or self.code == TransactionResultCode.txMISSING_OPERATION
            or self.code == TransactionResultCode.txBAD_SEQ
            or self.code == TransactionResultCode.txBAD_AUTH
            or self.code == TransactionResultCode.txINSUFFICIENT_BALANCE
            or self.code == TransactionResultCode.txNO_ACCOUNT
            or self.code == TransactionResultCode.txINSUFFICIENT_FEE
            or self.code == TransactionResultCode.txBAD_AUTH_EXTRA
            or self.code == TransactionResultCode.txINTERNAL_ERROR
            or self.code == TransactionResultCode.txNOT_SUPPORTED
            or self.code == TransactionResultCode.txBAD_SPONSORSHIP
        ):
            return
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "InnerTransactionResultResult":
        code = TransactionResultCode.unpack(unpacker)
        if (
            code == TransactionResultCode.txSUCCESS
            or code == TransactionResultCode.txFAILED
        ):
            length = unpacker.unpack_uint()
            results = []
            for _ in range(length):
                results.append(OperationResult.unpack(unpacker))
            return cls(code, results=results)
        if (
            code == TransactionResultCode.txTOO_EARLY
            or code == TransactionResultCode.txTOO_LATE
            or code == TransactionResultCode.txMISSING_OPERATION
            or code == TransactionResultCode.txBAD_SEQ
            or code == TransactionResultCode.txBAD_AUTH
            or code == TransactionResultCode.txINSUFFICIENT_BALANCE
            or code == TransactionResultCode.txNO_ACCOUNT
            or code == TransactionResultCode.txINSUFFICIENT_FEE
            or code == TransactionResultCode.txBAD_AUTH_EXTRA
            or code == TransactionResultCode.txINTERNAL_ERROR
            or code == TransactionResultCode.txNOT_SUPPORTED
            or code == TransactionResultCode.txBAD_SPONSORSHIP
        ):
            return cls(code)
        raise ValueError("Invalid code.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "InnerTransactionResultResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "InnerTransactionResultResult":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code and self.results == other.results

    def __str__(self):
        out = []
        out.append(f"code={self.code}")
        out.append(f"results={self.results}") if self.results is not None else None
        return f"<InnerTransactionResultResult {[', '.join(out)]}>"
