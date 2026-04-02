# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List, Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .operation_result import OperationResult
from .transaction_result_code import TransactionResultCode

__all__ = ["InnerTransactionResultResult"]


class InnerTransactionResultResult:
    """
    XDR Source Code::

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
            case txBAD_MIN_SEQ_AGE_OR_GAP:
            case txMALFORMED:
            case txSOROBAN_INVALID:
            case txFROZEN_KEY_ACCESSED:
                void;
            }
    """

    def __init__(
        self,
        code: TransactionResultCode,
        results: Optional[List[OperationResult]] = None,
    ) -> None:
        _expect_max_length = 4294967295
        if results and len(results) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `results` should be {_expect_max_length}, but got {len(results)}."
            )
        self.code = code
        self.results = results

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
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
        if self.code == TransactionResultCode.txSOROBAN_INVALID:
            return
        if self.code == TransactionResultCode.txFROZEN_KEY_ACCESSED:
            return
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> InnerTransactionResultResult:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        code = TransactionResultCode.unpack(unpacker)
        if code == TransactionResultCode.txSUCCESS:
            length = unpacker.unpack_uint()
            _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
            if _remaining < length:
                raise ValueError(
                    f"results length {length} exceeds remaining input length {_remaining}"
                )
            results = []
            for _ in range(length):
                results.append(OperationResult.unpack(unpacker, depth_limit - 1))
            return cls(code=code, results=results)
        if code == TransactionResultCode.txFAILED:
            length = unpacker.unpack_uint()
            _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
            if _remaining < length:
                raise ValueError(
                    f"results length {length} exceeds remaining input length {_remaining}"
                )
            results = []
            for _ in range(length):
                results.append(OperationResult.unpack(unpacker, depth_limit - 1))
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
        if code == TransactionResultCode.txSOROBAN_INVALID:
            return cls(code=code)
        if code == TransactionResultCode.txFROZEN_KEY_ACCESSED:
            return cls(code=code)
        raise ValueError("Invalid code.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> InnerTransactionResultResult:
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
    def from_xdr(cls, xdr: str) -> InnerTransactionResultResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> InnerTransactionResultResult:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.code == TransactionResultCode.txSUCCESS:
            assert self.results is not None
            return {"txsuccess": [item.to_json_dict() for item in self.results]}
        if self.code == TransactionResultCode.txFAILED:
            assert self.results is not None
            return {"txfailed": [item.to_json_dict() for item in self.results]}
        if self.code == TransactionResultCode.txTOO_EARLY:
            return "txtoo_early"
        if self.code == TransactionResultCode.txTOO_LATE:
            return "txtoo_late"
        if self.code == TransactionResultCode.txMISSING_OPERATION:
            return "txmissing_operation"
        if self.code == TransactionResultCode.txBAD_SEQ:
            return "txbad_seq"
        if self.code == TransactionResultCode.txBAD_AUTH:
            return "txbad_auth"
        if self.code == TransactionResultCode.txINSUFFICIENT_BALANCE:
            return "txinsufficient_balance"
        if self.code == TransactionResultCode.txNO_ACCOUNT:
            return "txno_account"
        if self.code == TransactionResultCode.txINSUFFICIENT_FEE:
            return "txinsufficient_fee"
        if self.code == TransactionResultCode.txBAD_AUTH_EXTRA:
            return "txbad_auth_extra"
        if self.code == TransactionResultCode.txINTERNAL_ERROR:
            return "txinternal_error"
        if self.code == TransactionResultCode.txNOT_SUPPORTED:
            return "txnot_supported"
        if self.code == TransactionResultCode.txBAD_SPONSORSHIP:
            return "txbad_sponsorship"
        if self.code == TransactionResultCode.txBAD_MIN_SEQ_AGE_OR_GAP:
            return "txbad_min_seq_age_or_gap"
        if self.code == TransactionResultCode.txMALFORMED:
            return "txmalformed"
        if self.code == TransactionResultCode.txSOROBAN_INVALID:
            return "txsoroban_invalid"
        if self.code == TransactionResultCode.txFROZEN_KEY_ACCESSED:
            return "txfrozen_key_accessed"
        raise ValueError(f"Unknown code in InnerTransactionResultResult: {self.code}")

    @classmethod
    def from_json_dict(cls, json_value: str | dict) -> InnerTransactionResultResult:
        if isinstance(json_value, str):
            if json_value not in (
                "txtoo_early",
                "txtoo_late",
                "txmissing_operation",
                "txbad_seq",
                "txbad_auth",
                "txinsufficient_balance",
                "txno_account",
                "txinsufficient_fee",
                "txbad_auth_extra",
                "txinternal_error",
                "txnot_supported",
                "txbad_sponsorship",
                "txbad_min_seq_age_or_gap",
                "txmalformed",
                "txsoroban_invalid",
                "txfrozen_key_accessed",
            ):
                raise ValueError(
                    f"Unexpected string '{json_value}' for InnerTransactionResultResult, must be one of: txtoo_early, txtoo_late, txmissing_operation, txbad_seq, txbad_auth, txinsufficient_balance, txno_account, txinsufficient_fee, txbad_auth_extra, txinternal_error, txnot_supported, txbad_sponsorship, txbad_min_seq_age_or_gap, txmalformed, txsoroban_invalid, txfrozen_key_accessed"
                )
            code = TransactionResultCode.from_json_dict(json_value)
            return cls(code=code)
        if not isinstance(json_value, dict) or len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for InnerTransactionResultResult, got: {json_value}"
            )
        key = next(iter(json_value))
        code = TransactionResultCode.from_json_dict(key)
        if key == "txsuccess":
            results = [
                OperationResult.from_json_dict(item) for item in json_value["txsuccess"]
            ]
            return cls(code=code, results=results)
        if key == "txfailed":
            results = [
                OperationResult.from_json_dict(item) for item in json_value["txfailed"]
            ]
            return cls(code=code, results=results)
        raise ValueError(f"Unknown key '{key}' for InnerTransactionResultResult")

    def __hash__(self):
        return hash(
            (
                self.code,
                self.results,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code and self.results == other.results

    def __repr__(self):
        out = []
        out.append(f"code={self.code}")
        if self.results is not None:
            out.append(f"results={self.results}")
        return f"<InnerTransactionResultResult [{', '.join(out)}]>"
