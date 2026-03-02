# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .operation_result_code import OperationResultCode
from .operation_result_tr import OperationResultTr

__all__ = ["OperationResult"]


class OperationResult:
    """
    XDR Source Code::

        union OperationResult switch (OperationResultCode code)
        {
        case opINNER:
            union switch (OperationType type)
            {
            case CREATE_ACCOUNT:
                CreateAccountResult createAccountResult;
            case PAYMENT:
                PaymentResult paymentResult;
            case PATH_PAYMENT_STRICT_RECEIVE:
                PathPaymentStrictReceiveResult pathPaymentStrictReceiveResult;
            case MANAGE_SELL_OFFER:
                ManageSellOfferResult manageSellOfferResult;
            case CREATE_PASSIVE_SELL_OFFER:
                ManageSellOfferResult createPassiveSellOfferResult;
            case SET_OPTIONS:
                SetOptionsResult setOptionsResult;
            case CHANGE_TRUST:
                ChangeTrustResult changeTrustResult;
            case ALLOW_TRUST:
                AllowTrustResult allowTrustResult;
            case ACCOUNT_MERGE:
                AccountMergeResult accountMergeResult;
            case INFLATION:
                InflationResult inflationResult;
            case MANAGE_DATA:
                ManageDataResult manageDataResult;
            case BUMP_SEQUENCE:
                BumpSequenceResult bumpSeqResult;
            case MANAGE_BUY_OFFER:
                ManageBuyOfferResult manageBuyOfferResult;
            case PATH_PAYMENT_STRICT_SEND:
                PathPaymentStrictSendResult pathPaymentStrictSendResult;
            case CREATE_CLAIMABLE_BALANCE:
                CreateClaimableBalanceResult createClaimableBalanceResult;
            case CLAIM_CLAIMABLE_BALANCE:
                ClaimClaimableBalanceResult claimClaimableBalanceResult;
            case BEGIN_SPONSORING_FUTURE_RESERVES:
                BeginSponsoringFutureReservesResult beginSponsoringFutureReservesResult;
            case END_SPONSORING_FUTURE_RESERVES:
                EndSponsoringFutureReservesResult endSponsoringFutureReservesResult;
            case REVOKE_SPONSORSHIP:
                RevokeSponsorshipResult revokeSponsorshipResult;
            case CLAWBACK:
                ClawbackResult clawbackResult;
            case CLAWBACK_CLAIMABLE_BALANCE:
                ClawbackClaimableBalanceResult clawbackClaimableBalanceResult;
            case SET_TRUST_LINE_FLAGS:
                SetTrustLineFlagsResult setTrustLineFlagsResult;
            case LIQUIDITY_POOL_DEPOSIT:
                LiquidityPoolDepositResult liquidityPoolDepositResult;
            case LIQUIDITY_POOL_WITHDRAW:
                LiquidityPoolWithdrawResult liquidityPoolWithdrawResult;
            case INVOKE_HOST_FUNCTION:
                InvokeHostFunctionResult invokeHostFunctionResult;
            case EXTEND_FOOTPRINT_TTL:
                ExtendFootprintTTLResult extendFootprintTTLResult;
            case RESTORE_FOOTPRINT:
                RestoreFootprintResult restoreFootprintResult;
            }
            tr;
        case opBAD_AUTH:
        case opNO_ACCOUNT:
        case opNOT_SUPPORTED:
        case opTOO_MANY_SUBENTRIES:
        case opEXCEEDED_WORK_LIMIT:
        case opTOO_MANY_SPONSORING:
            void;
        };
    """

    def __init__(
        self,
        code: OperationResultCode,
        tr: Optional[OperationResultTr] = None,
    ) -> None:
        self.code = code
        self.tr = tr

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == OperationResultCode.opINNER:
            if self.tr is None:
                raise ValueError("tr should not be None.")
            self.tr.pack(packer)
            return
        if self.code == OperationResultCode.opBAD_AUTH:
            return
        if self.code == OperationResultCode.opNO_ACCOUNT:
            return
        if self.code == OperationResultCode.opNOT_SUPPORTED:
            return
        if self.code == OperationResultCode.opTOO_MANY_SUBENTRIES:
            return
        if self.code == OperationResultCode.opEXCEEDED_WORK_LIMIT:
            return
        if self.code == OperationResultCode.opTOO_MANY_SPONSORING:
            return
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> OperationResult:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        code = OperationResultCode.unpack(unpacker)
        if code == OperationResultCode.opINNER:
            tr = OperationResultTr.unpack(unpacker, depth_limit - 1)
            return cls(code=code, tr=tr)
        if code == OperationResultCode.opBAD_AUTH:
            return cls(code=code)
        if code == OperationResultCode.opNO_ACCOUNT:
            return cls(code=code)
        if code == OperationResultCode.opNOT_SUPPORTED:
            return cls(code=code)
        if code == OperationResultCode.opTOO_MANY_SUBENTRIES:
            return cls(code=code)
        if code == OperationResultCode.opEXCEEDED_WORK_LIMIT:
            return cls(code=code)
        if code == OperationResultCode.opTOO_MANY_SPONSORING:
            return cls(code=code)
        raise ValueError("Invalid code.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> OperationResult:
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
    def from_xdr(cls, xdr: str) -> OperationResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> OperationResult:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.code == OperationResultCode.opINNER:
            assert self.tr is not None
            return {"opinner": self.tr.to_json_dict()}
        if self.code == OperationResultCode.opBAD_AUTH:
            return "opbad_auth"
        if self.code == OperationResultCode.opNO_ACCOUNT:
            return "opno_account"
        if self.code == OperationResultCode.opNOT_SUPPORTED:
            return "opnot_supported"
        if self.code == OperationResultCode.opTOO_MANY_SUBENTRIES:
            return "optoo_many_subentries"
        if self.code == OperationResultCode.opEXCEEDED_WORK_LIMIT:
            return "opexceeded_work_limit"
        if self.code == OperationResultCode.opTOO_MANY_SPONSORING:
            return "optoo_many_sponsoring"
        raise ValueError(f"Unknown code in OperationResult: {self.code}")

    @classmethod
    def from_json_dict(cls, json_value: str | dict) -> OperationResult:
        if isinstance(json_value, str):
            if json_value not in (
                "opbad_auth",
                "opno_account",
                "opnot_supported",
                "optoo_many_subentries",
                "opexceeded_work_limit",
                "optoo_many_sponsoring",
            ):
                raise ValueError(
                    f"Unexpected string '{json_value}' for OperationResult, must be one of: opbad_auth, opno_account, opnot_supported, optoo_many_subentries, opexceeded_work_limit, optoo_many_sponsoring"
                )
            code = OperationResultCode.from_json_dict(json_value)
            return cls(code=code)
        if not isinstance(json_value, dict) or len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for OperationResult, got: {json_value}"
            )
        key = next(iter(json_value))
        code = OperationResultCode.from_json_dict(key)
        if key == "opinner":
            tr = OperationResultTr.from_json_dict(json_value["opinner"])
            return cls(code=code, tr=tr)
        raise ValueError(f"Unknown key '{key}' for OperationResult")

    def __hash__(self):
        return hash(
            (
                self.code,
                self.tr,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code and self.tr == other.tr

    def __repr__(self):
        out = []
        out.append(f"code={self.code}")
        if self.tr is not None:
            out.append(f"tr={self.tr}")
        return f"<OperationResult [{', '.join(out)}]>"
