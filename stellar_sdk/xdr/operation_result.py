# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .operation_result_code import OperationResultCode
from .operation_result_tr import OperationResultTr
from ..exceptions import ValueError

__all__ = ["OperationResult"]


class OperationResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
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
        }
        tr;
    default:
        void;
    };
    ----------------------------------------------------------------
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
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "OperationResult":
        code = OperationResultCode.unpack(unpacker)
        if code == OperationResultCode.opINNER:
            tr = OperationResultTr.unpack(unpacker)
            if tr is None:
                raise ValueError("tr should not be None.")
            return cls(code, tr=tr)
        raise ValueError("Invalid code.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "OperationResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "OperationResult":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code and self.tr == other.tr

    def __str__(self):
        out = []
        out.append(f"code={self.code}")
        out.append(f"tr={self.tr}") if self.tr is not None else None
        return f"<OperationResult {[', '.join(out)]}>"
