# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .account_merge_result import AccountMergeResult
from .allow_trust_result import AllowTrustResult
from .begin_sponsoring_future_reserves_result import BeginSponsoringFutureReservesResult
from .bump_sequence_result import BumpSequenceResult
from .change_trust_result import ChangeTrustResult
from .claim_claimable_balance_result import ClaimClaimableBalanceResult
from .create_account_result import CreateAccountResult
from .create_claimable_balance_result import CreateClaimableBalanceResult
from .end_sponsoring_future_reserves_result import EndSponsoringFutureReservesResult
from .inflation_result import InflationResult
from .manage_buy_offer_result import ManageBuyOfferResult
from .manage_data_result import ManageDataResult
from .manage_sell_offer_result import ManageSellOfferResult
from .operation_type import OperationType
from .path_payment_strict_receive_result import PathPaymentStrictReceiveResult
from .path_payment_strict_send_result import PathPaymentStrictSendResult
from .payment_result import PaymentResult
from .revoke_sponsorship_result import RevokeSponsorshipResult
from .set_options_result import SetOptionsResult

__all__ = ["OperationResultTr"]


class OperationResultTr:
    """
    XDR Source Code
    ----------------------------------------------------------------
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
        }
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: OperationType,
        create_account_result: CreateAccountResult = None,
        payment_result: PaymentResult = None,
        path_payment_strict_receive_result: PathPaymentStrictReceiveResult = None,
        manage_sell_offer_result: ManageSellOfferResult = None,
        create_passive_sell_offer_result: ManageSellOfferResult = None,
        set_options_result: SetOptionsResult = None,
        change_trust_result: ChangeTrustResult = None,
        allow_trust_result: AllowTrustResult = None,
        account_merge_result: AccountMergeResult = None,
        inflation_result: InflationResult = None,
        manage_data_result: ManageDataResult = None,
        bump_seq_result: BumpSequenceResult = None,
        manage_buy_offer_result: ManageBuyOfferResult = None,
        path_payment_strict_send_result: PathPaymentStrictSendResult = None,
        create_claimable_balance_result: CreateClaimableBalanceResult = None,
        claim_claimable_balance_result: ClaimClaimableBalanceResult = None,
        begin_sponsoring_future_reserves_result: BeginSponsoringFutureReservesResult = None,
        end_sponsoring_future_reserves_result: EndSponsoringFutureReservesResult = None,
        revoke_sponsorship_result: RevokeSponsorshipResult = None,
    ) -> None:
        self.type = type
        self.create_account_result = create_account_result
        self.payment_result = payment_result
        self.path_payment_strict_receive_result = path_payment_strict_receive_result
        self.manage_sell_offer_result = manage_sell_offer_result
        self.create_passive_sell_offer_result = create_passive_sell_offer_result
        self.set_options_result = set_options_result
        self.change_trust_result = change_trust_result
        self.allow_trust_result = allow_trust_result
        self.account_merge_result = account_merge_result
        self.inflation_result = inflation_result
        self.manage_data_result = manage_data_result
        self.bump_seq_result = bump_seq_result
        self.manage_buy_offer_result = manage_buy_offer_result
        self.path_payment_strict_send_result = path_payment_strict_send_result
        self.create_claimable_balance_result = create_claimable_balance_result
        self.claim_claimable_balance_result = claim_claimable_balance_result
        self.begin_sponsoring_future_reserves_result = (
            begin_sponsoring_future_reserves_result
        )
        self.end_sponsoring_future_reserves_result = (
            end_sponsoring_future_reserves_result
        )
        self.revoke_sponsorship_result = revoke_sponsorship_result

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == OperationType.CREATE_ACCOUNT:
            self.create_account_result.pack(packer)
            return
        if self.type == OperationType.PAYMENT:
            self.payment_result.pack(packer)
            return
        if self.type == OperationType.PATH_PAYMENT_STRICT_RECEIVE:
            self.path_payment_strict_receive_result.pack(packer)
            return
        if self.type == OperationType.MANAGE_SELL_OFFER:
            self.manage_sell_offer_result.pack(packer)
            return
        if self.type == OperationType.CREATE_PASSIVE_SELL_OFFER:
            self.create_passive_sell_offer_result.pack(packer)
            return
        if self.type == OperationType.SET_OPTIONS:
            self.set_options_result.pack(packer)
            return
        if self.type == OperationType.CHANGE_TRUST:
            self.change_trust_result.pack(packer)
            return
        if self.type == OperationType.ALLOW_TRUST:
            self.allow_trust_result.pack(packer)
            return
        if self.type == OperationType.ACCOUNT_MERGE:
            self.account_merge_result.pack(packer)
            return
        if self.type == OperationType.INFLATION:
            self.inflation_result.pack(packer)
            return
        if self.type == OperationType.MANAGE_DATA:
            self.manage_data_result.pack(packer)
            return
        if self.type == OperationType.BUMP_SEQUENCE:
            self.bump_seq_result.pack(packer)
            return
        if self.type == OperationType.MANAGE_BUY_OFFER:
            self.manage_buy_offer_result.pack(packer)
            return
        if self.type == OperationType.PATH_PAYMENT_STRICT_SEND:
            self.path_payment_strict_send_result.pack(packer)
            return
        if self.type == OperationType.CREATE_CLAIMABLE_BALANCE:
            self.create_claimable_balance_result.pack(packer)
            return
        if self.type == OperationType.CLAIM_CLAIMABLE_BALANCE:
            self.claim_claimable_balance_result.pack(packer)
            return
        if self.type == OperationType.BEGIN_SPONSORING_FUTURE_RESERVES:
            self.begin_sponsoring_future_reserves_result.pack(packer)
            return
        if self.type == OperationType.END_SPONSORING_FUTURE_RESERVES:
            self.end_sponsoring_future_reserves_result.pack(packer)
            return
        if self.type == OperationType.REVOKE_SPONSORSHIP:
            self.revoke_sponsorship_result.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "OperationResultTr":
        type = OperationType.unpack(unpacker)
        if type == OperationType.CREATE_ACCOUNT:
            create_account_result = CreateAccountResult.unpack(unpacker)
            return cls(type, create_account_result=create_account_result)
        if type == OperationType.PAYMENT:
            payment_result = PaymentResult.unpack(unpacker)
            return cls(type, payment_result=payment_result)
        if type == OperationType.PATH_PAYMENT_STRICT_RECEIVE:
            path_payment_strict_receive_result = PathPaymentStrictReceiveResult.unpack(
                unpacker
            )
            return cls(
                type,
                path_payment_strict_receive_result=path_payment_strict_receive_result,
            )
        if type == OperationType.MANAGE_SELL_OFFER:
            manage_sell_offer_result = ManageSellOfferResult.unpack(unpacker)
            return cls(type, manage_sell_offer_result=manage_sell_offer_result)
        if type == OperationType.CREATE_PASSIVE_SELL_OFFER:
            create_passive_sell_offer_result = ManageSellOfferResult.unpack(unpacker)
            return cls(
                type, create_passive_sell_offer_result=create_passive_sell_offer_result
            )
        if type == OperationType.SET_OPTIONS:
            set_options_result = SetOptionsResult.unpack(unpacker)
            return cls(type, set_options_result=set_options_result)
        if type == OperationType.CHANGE_TRUST:
            change_trust_result = ChangeTrustResult.unpack(unpacker)
            return cls(type, change_trust_result=change_trust_result)
        if type == OperationType.ALLOW_TRUST:
            allow_trust_result = AllowTrustResult.unpack(unpacker)
            return cls(type, allow_trust_result=allow_trust_result)
        if type == OperationType.ACCOUNT_MERGE:
            account_merge_result = AccountMergeResult.unpack(unpacker)
            return cls(type, account_merge_result=account_merge_result)
        if type == OperationType.INFLATION:
            inflation_result = InflationResult.unpack(unpacker)
            return cls(type, inflation_result=inflation_result)
        if type == OperationType.MANAGE_DATA:
            manage_data_result = ManageDataResult.unpack(unpacker)
            return cls(type, manage_data_result=manage_data_result)
        if type == OperationType.BUMP_SEQUENCE:
            bump_seq_result = BumpSequenceResult.unpack(unpacker)
            return cls(type, bump_seq_result=bump_seq_result)
        if type == OperationType.MANAGE_BUY_OFFER:
            manage_buy_offer_result = ManageBuyOfferResult.unpack(unpacker)
            return cls(type, manage_buy_offer_result=manage_buy_offer_result)
        if type == OperationType.PATH_PAYMENT_STRICT_SEND:
            path_payment_strict_send_result = PathPaymentStrictSendResult.unpack(
                unpacker
            )
            return cls(
                type, path_payment_strict_send_result=path_payment_strict_send_result
            )
        if type == OperationType.CREATE_CLAIMABLE_BALANCE:
            create_claimable_balance_result = CreateClaimableBalanceResult.unpack(
                unpacker
            )
            return cls(
                type, create_claimable_balance_result=create_claimable_balance_result
            )
        if type == OperationType.CLAIM_CLAIMABLE_BALANCE:
            claim_claimable_balance_result = ClaimClaimableBalanceResult.unpack(
                unpacker
            )
            return cls(
                type, claim_claimable_balance_result=claim_claimable_balance_result
            )
        if type == OperationType.BEGIN_SPONSORING_FUTURE_RESERVES:
            begin_sponsoring_future_reserves_result = BeginSponsoringFutureReservesResult.unpack(
                unpacker
            )
            return cls(
                type,
                begin_sponsoring_future_reserves_result=begin_sponsoring_future_reserves_result,
            )
        if type == OperationType.END_SPONSORING_FUTURE_RESERVES:
            end_sponsoring_future_reserves_result = EndSponsoringFutureReservesResult.unpack(
                unpacker
            )
            return cls(
                type,
                end_sponsoring_future_reserves_result=end_sponsoring_future_reserves_result,
            )
        if type == OperationType.REVOKE_SPONSORSHIP:
            revoke_sponsorship_result = RevokeSponsorshipResult.unpack(unpacker)
            return cls(type, revoke_sponsorship_result=revoke_sponsorship_result)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "OperationResultTr":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "OperationResultTr":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.create_account_result == other.create_account_result
            and self.payment_result == other.payment_result
            and self.path_payment_strict_receive_result
            == other.path_payment_strict_receive_result
            and self.manage_sell_offer_result == other.manage_sell_offer_result
            and self.create_passive_sell_offer_result
            == other.create_passive_sell_offer_result
            and self.set_options_result == other.set_options_result
            and self.change_trust_result == other.change_trust_result
            and self.allow_trust_result == other.allow_trust_result
            and self.account_merge_result == other.account_merge_result
            and self.inflation_result == other.inflation_result
            and self.manage_data_result == other.manage_data_result
            and self.bump_seq_result == other.bump_seq_result
            and self.manage_buy_offer_result == other.manage_buy_offer_result
            and self.path_payment_strict_send_result
            == other.path_payment_strict_send_result
            and self.create_claimable_balance_result
            == other.create_claimable_balance_result
            and self.claim_claimable_balance_result
            == other.claim_claimable_balance_result
            and self.begin_sponsoring_future_reserves_result
            == other.begin_sponsoring_future_reserves_result
            and self.end_sponsoring_future_reserves_result
            == other.end_sponsoring_future_reserves_result
            and self.revoke_sponsorship_result == other.revoke_sponsorship_result
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(
            f"create_account_result={self.create_account_result}"
        ) if self.create_account_result is not None else None
        out.append(
            f"payment_result={self.payment_result}"
        ) if self.payment_result is not None else None
        out.append(
            f"path_payment_strict_receive_result={self.path_payment_strict_receive_result}"
        ) if self.path_payment_strict_receive_result is not None else None
        out.append(
            f"manage_sell_offer_result={self.manage_sell_offer_result}"
        ) if self.manage_sell_offer_result is not None else None
        out.append(
            f"create_passive_sell_offer_result={self.create_passive_sell_offer_result}"
        ) if self.create_passive_sell_offer_result is not None else None
        out.append(
            f"set_options_result={self.set_options_result}"
        ) if self.set_options_result is not None else None
        out.append(
            f"change_trust_result={self.change_trust_result}"
        ) if self.change_trust_result is not None else None
        out.append(
            f"allow_trust_result={self.allow_trust_result}"
        ) if self.allow_trust_result is not None else None
        out.append(
            f"account_merge_result={self.account_merge_result}"
        ) if self.account_merge_result is not None else None
        out.append(
            f"inflation_result={self.inflation_result}"
        ) if self.inflation_result is not None else None
        out.append(
            f"manage_data_result={self.manage_data_result}"
        ) if self.manage_data_result is not None else None
        out.append(
            f"bump_seq_result={self.bump_seq_result}"
        ) if self.bump_seq_result is not None else None
        out.append(
            f"manage_buy_offer_result={self.manage_buy_offer_result}"
        ) if self.manage_buy_offer_result is not None else None
        out.append(
            f"path_payment_strict_send_result={self.path_payment_strict_send_result}"
        ) if self.path_payment_strict_send_result is not None else None
        out.append(
            f"create_claimable_balance_result={self.create_claimable_balance_result}"
        ) if self.create_claimable_balance_result is not None else None
        out.append(
            f"claim_claimable_balance_result={self.claim_claimable_balance_result}"
        ) if self.claim_claimable_balance_result is not None else None
        out.append(
            f"begin_sponsoring_future_reserves_result={self.begin_sponsoring_future_reserves_result}"
        ) if self.begin_sponsoring_future_reserves_result is not None else None
        out.append(
            f"end_sponsoring_future_reserves_result={self.end_sponsoring_future_reserves_result}"
        ) if self.end_sponsoring_future_reserves_result is not None else None
        out.append(
            f"revoke_sponsorship_result={self.revoke_sponsorship_result}"
        ) if self.revoke_sponsorship_result is not None else None
        return f"<OperationResultTr {[', '.join(out)]}>"
