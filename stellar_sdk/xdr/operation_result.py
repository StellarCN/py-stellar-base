# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

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
        tr: OperationResultTr = None,
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

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> OperationResult:
        code = OperationResultCode.unpack(unpacker)
        if code == OperationResultCode.opINNER:
            tr = OperationResultTr.unpack(unpacker)
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
        return cls(code=code)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> OperationResult:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> OperationResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
        out.append(f"tr={self.tr}") if self.tr is not None else None
        return f"<OperationResult [{', '.join(out)}]>"
