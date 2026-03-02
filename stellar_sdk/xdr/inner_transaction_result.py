# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .inner_transaction_result_ext import InnerTransactionResultExt
from .inner_transaction_result_result import InnerTransactionResultResult
from .int64 import Int64

__all__ = ["InnerTransactionResult"]


class InnerTransactionResult:
    """
    XDR Source Code::

        struct InnerTransactionResult
        {
            // Always 0. Here for binary compatibility.
            int64 feeCharged;

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
    """

    def __init__(
        self,
        fee_charged: Int64,
        result: InnerTransactionResultResult,
        ext: InnerTransactionResultExt,
    ) -> None:
        self.fee_charged = fee_charged
        self.result = result
        self.ext = ext

    def pack(self, packer: Packer) -> None:
        self.fee_charged.pack(packer)
        self.result.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> InnerTransactionResult:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        fee_charged = Int64.unpack(unpacker, depth_limit - 1)
        result = InnerTransactionResultResult.unpack(unpacker, depth_limit - 1)
        ext = InnerTransactionResultExt.unpack(unpacker, depth_limit - 1)
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
    def from_xdr_bytes(cls, xdr: bytes) -> InnerTransactionResult:
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
    def from_xdr(cls, xdr: str) -> InnerTransactionResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> InnerTransactionResult:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "fee_charged": self.fee_charged.to_json_dict(),
            "result": self.result.to_json_dict(),
            "ext": self.ext.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> InnerTransactionResult:
        fee_charged = Int64.from_json_dict(json_dict["fee_charged"])
        result = InnerTransactionResultResult.from_json_dict(json_dict["result"])
        ext = InnerTransactionResultExt.from_json_dict(json_dict["ext"])
        return cls(
            fee_charged=fee_charged,
            result=result,
            ext=ext,
        )

    def __hash__(self):
        return hash(
            (
                self.fee_charged,
                self.result,
                self.ext,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.fee_charged == other.fee_charged
            and self.result == other.result
            and self.ext == other.ext
        )

    def __repr__(self):
        out = [
            f"fee_charged={self.fee_charged}",
            f"result={self.result}",
            f"ext={self.ext}",
        ]
        return f"<InnerTransactionResult [{', '.join(out)}]>"
