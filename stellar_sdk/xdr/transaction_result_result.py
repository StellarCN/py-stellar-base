# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib3 import Packer, Unpacker

from .inner_transaction_result_pair import InnerTransactionResultPair
from .operation_result import OperationResult
from .transaction_result_code import TransactionResultCode

__all__ = ["TransactionResultResult"]


class TransactionResultResult:
    """
    XDR Source Code::

        union switch (TransactionResultCode code)
            {
            case txFEE_BUMP_INNER_SUCCESS:
            case txFEE_BUMP_INNER_FAILED:
                InnerTransactionResultPair innerResultPair;
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
            // case txFEE_BUMP_INNER_FAILED: handled above
            case txBAD_SPONSORSHIP:
            case txBAD_MIN_SEQ_AGE_OR_GAP:
            case txMALFORMED:
            case txSOROBAN_RESOURCE_LIMIT_EXCEEDED:
                void;
            }
    """

    def __init__(
        self,
        code: TransactionResultCode,
        inner_result_pair: InnerTransactionResultPair = None,
        results: List[OperationResult] = None,
    ) -> None:
        _expect_max_length = 4294967295
        if results and len(results) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `results` should be {_expect_max_length}, but got {len(results)}."
            )
        self.code = code
        self.inner_result_pair = inner_result_pair
        self.results = results

    @classmethod
    def from_tx_fee_bump_inner_success(
        cls, inner_result_pair: InnerTransactionResultPair
    ) -> "TransactionResultResult":
        return cls(
            TransactionResultCode.txFEE_BUMP_INNER_SUCCESS,
            inner_result_pair=inner_result_pair,
        )

    @classmethod
    def from_tx_fee_bump_inner_failed(
        cls, inner_result_pair: InnerTransactionResultPair
    ) -> "TransactionResultResult":
        return cls(
            TransactionResultCode.txFEE_BUMP_INNER_FAILED,
            inner_result_pair=inner_result_pair,
        )

    @classmethod
    def from_tx_success(
        cls, results: List[OperationResult]
    ) -> "TransactionResultResult":
        return cls(TransactionResultCode.txSUCCESS, results=results)

    @classmethod
    def from_tx_failed(
        cls, results: List[OperationResult]
    ) -> "TransactionResultResult":
        return cls(TransactionResultCode.txFAILED, results=results)

    @classmethod
    def from_tx_too_early(cls) -> "TransactionResultResult":
        return cls(TransactionResultCode.txTOO_EARLY)

    @classmethod
    def from_tx_too_late(cls) -> "TransactionResultResult":
        return cls(TransactionResultCode.txTOO_LATE)

    @classmethod
    def from_tx_missing_operation(cls) -> "TransactionResultResult":
        return cls(TransactionResultCode.txMISSING_OPERATION)

    @classmethod
    def from_tx_bad_seq(cls) -> "TransactionResultResult":
        return cls(TransactionResultCode.txBAD_SEQ)

    @classmethod
    def from_tx_bad_auth(cls) -> "TransactionResultResult":
        return cls(TransactionResultCode.txBAD_AUTH)

    @classmethod
    def from_tx_insufficient_balance(cls) -> "TransactionResultResult":
        return cls(TransactionResultCode.txINSUFFICIENT_BALANCE)

    @classmethod
    def from_tx_no_account(cls) -> "TransactionResultResult":
        return cls(TransactionResultCode.txNO_ACCOUNT)

    @classmethod
    def from_tx_insufficient_fee(cls) -> "TransactionResultResult":
        return cls(TransactionResultCode.txINSUFFICIENT_FEE)

    @classmethod
    def from_tx_bad_auth_extra(cls) -> "TransactionResultResult":
        return cls(TransactionResultCode.txBAD_AUTH_EXTRA)

    @classmethod
    def from_tx_internal_error(cls) -> "TransactionResultResult":
        return cls(TransactionResultCode.txINTERNAL_ERROR)

    @classmethod
    def from_tx_not_supported(cls) -> "TransactionResultResult":
        return cls(TransactionResultCode.txNOT_SUPPORTED)

    @classmethod
    def from_tx_bad_sponsorship(cls) -> "TransactionResultResult":
        return cls(TransactionResultCode.txBAD_SPONSORSHIP)

    @classmethod
    def from_tx_bad_min_seq_age_or_gap(cls) -> "TransactionResultResult":
        return cls(TransactionResultCode.txBAD_MIN_SEQ_AGE_OR_GAP)

    @classmethod
    def from_tx_malformed(cls) -> "TransactionResultResult":
        return cls(TransactionResultCode.txMALFORMED)

    @classmethod
    def from_tx_soroban_resource_limit_exceeded(cls) -> "TransactionResultResult":
        return cls(TransactionResultCode.txSOROBAN_RESOURCE_LIMIT_EXCEEDED)

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == TransactionResultCode.txFEE_BUMP_INNER_SUCCESS:
            if self.inner_result_pair is None:
                raise ValueError("inner_result_pair should not be None.")
            self.inner_result_pair.pack(packer)
            return
        if self.code == TransactionResultCode.txFEE_BUMP_INNER_FAILED:
            if self.inner_result_pair is None:
                raise ValueError("inner_result_pair should not be None.")
            self.inner_result_pair.pack(packer)
            return
        if self.code == TransactionResultCode.txSUCCESS:
            if self.results is None:
                raise ValueError("results should not be None.")
            packer.pack_uint(len(self.results))
            for results_item in self.results:
                results_item.pack(packer)
            return
        if self.code == TransactionResultCode.txFAILED:
            if self.results is None:
                raise ValueError("results should not be None.")
            packer.pack_uint(len(self.results))
            for results_item in self.results:
                results_item.pack(packer)
            return
        if self.code == TransactionResultCode.txTOO_EARLY:
            return
        if self.code == TransactionResultCode.txTOO_LATE:
            return
        if self.code == TransactionResultCode.txMISSING_OPERATION:
            return
        if self.code == TransactionResultCode.txBAD_SEQ:
            return
        if self.code == TransactionResultCode.txBAD_AUTH:
            return
        if self.code == TransactionResultCode.txINSUFFICIENT_BALANCE:
            return
        if self.code == TransactionResultCode.txNO_ACCOUNT:
            return
        if self.code == TransactionResultCode.txINSUFFICIENT_FEE:
            return
        if self.code == TransactionResultCode.txBAD_AUTH_EXTRA:
            return
        if self.code == TransactionResultCode.txINTERNAL_ERROR:
            return
        if self.code == TransactionResultCode.txNOT_SUPPORTED:
            return
        if self.code == TransactionResultCode.txBAD_SPONSORSHIP:
            return
        if self.code == TransactionResultCode.txBAD_MIN_SEQ_AGE_OR_GAP:
            return
        if self.code == TransactionResultCode.txMALFORMED:
            return
        if self.code == TransactionResultCode.txSOROBAN_RESOURCE_LIMIT_EXCEEDED:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionResultResult":
        code = TransactionResultCode.unpack(unpacker)
        if code == TransactionResultCode.txFEE_BUMP_INNER_SUCCESS:
            inner_result_pair = InnerTransactionResultPair.unpack(unpacker)
            return cls(code=code, inner_result_pair=inner_result_pair)
        if code == TransactionResultCode.txFEE_BUMP_INNER_FAILED:
            inner_result_pair = InnerTransactionResultPair.unpack(unpacker)
            return cls(code=code, inner_result_pair=inner_result_pair)
        if code == TransactionResultCode.txSUCCESS:
            length = unpacker.unpack_uint()
            results = []
            for _ in range(length):
                results.append(OperationResult.unpack(unpacker))
            return cls(code=code, results=results)
        if code == TransactionResultCode.txFAILED:
            length = unpacker.unpack_uint()
            results = []
            for _ in range(length):
                results.append(OperationResult.unpack(unpacker))
            return cls(code=code, results=results)
        if code == TransactionResultCode.txTOO_EARLY:
            return cls(code=code)
        if code == TransactionResultCode.txTOO_LATE:
            return cls(code=code)
        if code == TransactionResultCode.txMISSING_OPERATION:
            return cls(code=code)
        if code == TransactionResultCode.txBAD_SEQ:
            return cls(code=code)
        if code == TransactionResultCode.txBAD_AUTH:
            return cls(code=code)
        if code == TransactionResultCode.txINSUFFICIENT_BALANCE:
            return cls(code=code)
        if code == TransactionResultCode.txNO_ACCOUNT:
            return cls(code=code)
        if code == TransactionResultCode.txINSUFFICIENT_FEE:
            return cls(code=code)
        if code == TransactionResultCode.txBAD_AUTH_EXTRA:
            return cls(code=code)
        if code == TransactionResultCode.txINTERNAL_ERROR:
            return cls(code=code)
        if code == TransactionResultCode.txNOT_SUPPORTED:
            return cls(code=code)
        if code == TransactionResultCode.txBAD_SPONSORSHIP:
            return cls(code=code)
        if code == TransactionResultCode.txBAD_MIN_SEQ_AGE_OR_GAP:
            return cls(code=code)
        if code == TransactionResultCode.txMALFORMED:
            return cls(code=code)
        if code == TransactionResultCode.txSOROBAN_RESOURCE_LIMIT_EXCEEDED:
            return cls(code=code)
        return cls(code=code)

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
        return f"<TransactionResultResult [{', '.join(out)}]>"
