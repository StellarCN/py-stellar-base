# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from ..exceptions import ValueError
from .allow_trust_op import AllowTrustOp
from .begin_sponsoring_future_reserves_op import BeginSponsoringFutureReservesOp
from .bump_sequence_op import BumpSequenceOp
from .change_trust_op import ChangeTrustOp
from .claim_claimable_balance_op import ClaimClaimableBalanceOp
from .clawback_claimable_balance_op import ClawbackClaimableBalanceOp
from .clawback_op import ClawbackOp
from .create_account_op import CreateAccountOp
from .create_claimable_balance_op import CreateClaimableBalanceOp
from .create_passive_sell_offer_op import CreatePassiveSellOfferOp
from .manage_buy_offer_op import ManageBuyOfferOp
from .manage_data_op import ManageDataOp
from .manage_sell_offer_op import ManageSellOfferOp
from .muxed_account import MuxedAccount
from .operation_type import OperationType
from .path_payment_strict_receive_op import PathPaymentStrictReceiveOp
from .path_payment_strict_send_op import PathPaymentStrictSendOp
from .payment_op import PaymentOp
from .revoke_sponsorship_op import RevokeSponsorshipOp
from .set_options_op import SetOptionsOp
from .set_trust_line_flags_op import SetTrustLineFlagsOp

__all__ = ["OperationBody"]


class OperationBody:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (OperationType type)
        {
        case CREATE_ACCOUNT:
            CreateAccountOp createAccountOp;
        case PAYMENT:
            PaymentOp paymentOp;
        case PATH_PAYMENT_STRICT_RECEIVE:
            PathPaymentStrictReceiveOp pathPaymentStrictReceiveOp;
        case MANAGE_SELL_OFFER:
            ManageSellOfferOp manageSellOfferOp;
        case CREATE_PASSIVE_SELL_OFFER:
            CreatePassiveSellOfferOp createPassiveSellOfferOp;
        case SET_OPTIONS:
            SetOptionsOp setOptionsOp;
        case CHANGE_TRUST:
            ChangeTrustOp changeTrustOp;
        case ALLOW_TRUST:
            AllowTrustOp allowTrustOp;
        case ACCOUNT_MERGE:
            MuxedAccount destination;
        case INFLATION:
            void;
        case MANAGE_DATA:
            ManageDataOp manageDataOp;
        case BUMP_SEQUENCE:
            BumpSequenceOp bumpSequenceOp;
        case MANAGE_BUY_OFFER:
            ManageBuyOfferOp manageBuyOfferOp;
        case PATH_PAYMENT_STRICT_SEND:
            PathPaymentStrictSendOp pathPaymentStrictSendOp;
        case CREATE_CLAIMABLE_BALANCE:
            CreateClaimableBalanceOp createClaimableBalanceOp;
        case CLAIM_CLAIMABLE_BALANCE:
            ClaimClaimableBalanceOp claimClaimableBalanceOp;
        case BEGIN_SPONSORING_FUTURE_RESERVES:
            BeginSponsoringFutureReservesOp beginSponsoringFutureReservesOp;
        case END_SPONSORING_FUTURE_RESERVES:
            void;
        case REVOKE_SPONSORSHIP:
            RevokeSponsorshipOp revokeSponsorshipOp;
        case CLAWBACK:
            ClawbackOp clawbackOp;
        case CLAWBACK_CLAIMABLE_BALANCE:
            ClawbackClaimableBalanceOp clawbackClaimableBalanceOp;
        case SET_TRUST_LINE_FLAGS:
            SetTrustLineFlagsOp setTrustLineFlagsOp;
        }
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: OperationType,
        create_account_op: CreateAccountOp = None,
        payment_op: PaymentOp = None,
        path_payment_strict_receive_op: PathPaymentStrictReceiveOp = None,
        manage_sell_offer_op: ManageSellOfferOp = None,
        create_passive_sell_offer_op: CreatePassiveSellOfferOp = None,
        set_options_op: SetOptionsOp = None,
        change_trust_op: ChangeTrustOp = None,
        allow_trust_op: AllowTrustOp = None,
        destination: MuxedAccount = None,
        manage_data_op: ManageDataOp = None,
        bump_sequence_op: BumpSequenceOp = None,
        manage_buy_offer_op: ManageBuyOfferOp = None,
        path_payment_strict_send_op: PathPaymentStrictSendOp = None,
        create_claimable_balance_op: CreateClaimableBalanceOp = None,
        claim_claimable_balance_op: ClaimClaimableBalanceOp = None,
        begin_sponsoring_future_reserves_op: BeginSponsoringFutureReservesOp = None,
        revoke_sponsorship_op: RevokeSponsorshipOp = None,
        clawback_op: ClawbackOp = None,
        clawback_claimable_balance_op: ClawbackClaimableBalanceOp = None,
        set_trust_line_flags_op: SetTrustLineFlagsOp = None,
    ) -> None:
        self.type = type
        self.create_account_op = create_account_op
        self.payment_op = payment_op
        self.path_payment_strict_receive_op = path_payment_strict_receive_op
        self.manage_sell_offer_op = manage_sell_offer_op
        self.create_passive_sell_offer_op = create_passive_sell_offer_op
        self.set_options_op = set_options_op
        self.change_trust_op = change_trust_op
        self.allow_trust_op = allow_trust_op
        self.destination = destination
        self.manage_data_op = manage_data_op
        self.bump_sequence_op = bump_sequence_op
        self.manage_buy_offer_op = manage_buy_offer_op
        self.path_payment_strict_send_op = path_payment_strict_send_op
        self.create_claimable_balance_op = create_claimable_balance_op
        self.claim_claimable_balance_op = claim_claimable_balance_op
        self.begin_sponsoring_future_reserves_op = begin_sponsoring_future_reserves_op
        self.revoke_sponsorship_op = revoke_sponsorship_op
        self.clawback_op = clawback_op
        self.clawback_claimable_balance_op = clawback_claimable_balance_op
        self.set_trust_line_flags_op = set_trust_line_flags_op

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == OperationType.CREATE_ACCOUNT:
            if self.create_account_op is None:
                raise ValueError("create_account_op should not be None.")
            self.create_account_op.pack(packer)
            return
        if self.type == OperationType.PAYMENT:
            if self.payment_op is None:
                raise ValueError("payment_op should not be None.")
            self.payment_op.pack(packer)
            return
        if self.type == OperationType.PATH_PAYMENT_STRICT_RECEIVE:
            if self.path_payment_strict_receive_op is None:
                raise ValueError("path_payment_strict_receive_op should not be None.")
            self.path_payment_strict_receive_op.pack(packer)
            return
        if self.type == OperationType.MANAGE_SELL_OFFER:
            if self.manage_sell_offer_op is None:
                raise ValueError("manage_sell_offer_op should not be None.")
            self.manage_sell_offer_op.pack(packer)
            return
        if self.type == OperationType.CREATE_PASSIVE_SELL_OFFER:
            if self.create_passive_sell_offer_op is None:
                raise ValueError("create_passive_sell_offer_op should not be None.")
            self.create_passive_sell_offer_op.pack(packer)
            return
        if self.type == OperationType.SET_OPTIONS:
            if self.set_options_op is None:
                raise ValueError("set_options_op should not be None.")
            self.set_options_op.pack(packer)
            return
        if self.type == OperationType.CHANGE_TRUST:
            if self.change_trust_op is None:
                raise ValueError("change_trust_op should not be None.")
            self.change_trust_op.pack(packer)
            return
        if self.type == OperationType.ALLOW_TRUST:
            if self.allow_trust_op is None:
                raise ValueError("allow_trust_op should not be None.")
            self.allow_trust_op.pack(packer)
            return
        if self.type == OperationType.ACCOUNT_MERGE:
            if self.destination is None:
                raise ValueError("destination should not be None.")
            self.destination.pack(packer)
            return
        if self.type == OperationType.INFLATION:
            return
        if self.type == OperationType.MANAGE_DATA:
            if self.manage_data_op is None:
                raise ValueError("manage_data_op should not be None.")
            self.manage_data_op.pack(packer)
            return
        if self.type == OperationType.BUMP_SEQUENCE:
            if self.bump_sequence_op is None:
                raise ValueError("bump_sequence_op should not be None.")
            self.bump_sequence_op.pack(packer)
            return
        if self.type == OperationType.MANAGE_BUY_OFFER:
            if self.manage_buy_offer_op is None:
                raise ValueError("manage_buy_offer_op should not be None.")
            self.manage_buy_offer_op.pack(packer)
            return
        if self.type == OperationType.PATH_PAYMENT_STRICT_SEND:
            if self.path_payment_strict_send_op is None:
                raise ValueError("path_payment_strict_send_op should not be None.")
            self.path_payment_strict_send_op.pack(packer)
            return
        if self.type == OperationType.CREATE_CLAIMABLE_BALANCE:
            if self.create_claimable_balance_op is None:
                raise ValueError("create_claimable_balance_op should not be None.")
            self.create_claimable_balance_op.pack(packer)
            return
        if self.type == OperationType.CLAIM_CLAIMABLE_BALANCE:
            if self.claim_claimable_balance_op is None:
                raise ValueError("claim_claimable_balance_op should not be None.")
            self.claim_claimable_balance_op.pack(packer)
            return
        if self.type == OperationType.BEGIN_SPONSORING_FUTURE_RESERVES:
            if self.begin_sponsoring_future_reserves_op is None:
                raise ValueError(
                    "begin_sponsoring_future_reserves_op should not be None."
                )
            self.begin_sponsoring_future_reserves_op.pack(packer)
            return
        if self.type == OperationType.END_SPONSORING_FUTURE_RESERVES:
            return
        if self.type == OperationType.REVOKE_SPONSORSHIP:
            if self.revoke_sponsorship_op is None:
                raise ValueError("revoke_sponsorship_op should not be None.")
            self.revoke_sponsorship_op.pack(packer)
            return
        if self.type == OperationType.CLAWBACK:
            if self.clawback_op is None:
                raise ValueError("clawback_op should not be None.")
            self.clawback_op.pack(packer)
            return
        if self.type == OperationType.CLAWBACK_CLAIMABLE_BALANCE:
            if self.clawback_claimable_balance_op is None:
                raise ValueError("clawback_claimable_balance_op should not be None.")
            self.clawback_claimable_balance_op.pack(packer)
            return
        if self.type == OperationType.SET_TRUST_LINE_FLAGS:
            if self.set_trust_line_flags_op is None:
                raise ValueError("set_trust_line_flags_op should not be None.")
            self.set_trust_line_flags_op.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "OperationBody":
        type = OperationType.unpack(unpacker)
        if type == OperationType.CREATE_ACCOUNT:
            create_account_op = CreateAccountOp.unpack(unpacker)
            if create_account_op is None:
                raise ValueError("create_account_op should not be None.")
            return cls(type, create_account_op=create_account_op)
        if type == OperationType.PAYMENT:
            payment_op = PaymentOp.unpack(unpacker)
            if payment_op is None:
                raise ValueError("payment_op should not be None.")
            return cls(type, payment_op=payment_op)
        if type == OperationType.PATH_PAYMENT_STRICT_RECEIVE:
            path_payment_strict_receive_op = PathPaymentStrictReceiveOp.unpack(unpacker)
            if path_payment_strict_receive_op is None:
                raise ValueError("path_payment_strict_receive_op should not be None.")
            return cls(
                type, path_payment_strict_receive_op=path_payment_strict_receive_op
            )
        if type == OperationType.MANAGE_SELL_OFFER:
            manage_sell_offer_op = ManageSellOfferOp.unpack(unpacker)
            if manage_sell_offer_op is None:
                raise ValueError("manage_sell_offer_op should not be None.")
            return cls(type, manage_sell_offer_op=manage_sell_offer_op)
        if type == OperationType.CREATE_PASSIVE_SELL_OFFER:
            create_passive_sell_offer_op = CreatePassiveSellOfferOp.unpack(unpacker)
            if create_passive_sell_offer_op is None:
                raise ValueError("create_passive_sell_offer_op should not be None.")
            return cls(type, create_passive_sell_offer_op=create_passive_sell_offer_op)
        if type == OperationType.SET_OPTIONS:
            set_options_op = SetOptionsOp.unpack(unpacker)
            if set_options_op is None:
                raise ValueError("set_options_op should not be None.")
            return cls(type, set_options_op=set_options_op)
        if type == OperationType.CHANGE_TRUST:
            change_trust_op = ChangeTrustOp.unpack(unpacker)
            if change_trust_op is None:
                raise ValueError("change_trust_op should not be None.")
            return cls(type, change_trust_op=change_trust_op)
        if type == OperationType.ALLOW_TRUST:
            allow_trust_op = AllowTrustOp.unpack(unpacker)
            if allow_trust_op is None:
                raise ValueError("allow_trust_op should not be None.")
            return cls(type, allow_trust_op=allow_trust_op)
        if type == OperationType.ACCOUNT_MERGE:
            destination = MuxedAccount.unpack(unpacker)
            if destination is None:
                raise ValueError("destination should not be None.")
            return cls(type, destination=destination)
        if type == OperationType.INFLATION:
            return cls(type)
        if type == OperationType.MANAGE_DATA:
            manage_data_op = ManageDataOp.unpack(unpacker)
            if manage_data_op is None:
                raise ValueError("manage_data_op should not be None.")
            return cls(type, manage_data_op=manage_data_op)
        if type == OperationType.BUMP_SEQUENCE:
            bump_sequence_op = BumpSequenceOp.unpack(unpacker)
            if bump_sequence_op is None:
                raise ValueError("bump_sequence_op should not be None.")
            return cls(type, bump_sequence_op=bump_sequence_op)
        if type == OperationType.MANAGE_BUY_OFFER:
            manage_buy_offer_op = ManageBuyOfferOp.unpack(unpacker)
            if manage_buy_offer_op is None:
                raise ValueError("manage_buy_offer_op should not be None.")
            return cls(type, manage_buy_offer_op=manage_buy_offer_op)
        if type == OperationType.PATH_PAYMENT_STRICT_SEND:
            path_payment_strict_send_op = PathPaymentStrictSendOp.unpack(unpacker)
            if path_payment_strict_send_op is None:
                raise ValueError("path_payment_strict_send_op should not be None.")
            return cls(type, path_payment_strict_send_op=path_payment_strict_send_op)
        if type == OperationType.CREATE_CLAIMABLE_BALANCE:
            create_claimable_balance_op = CreateClaimableBalanceOp.unpack(unpacker)
            if create_claimable_balance_op is None:
                raise ValueError("create_claimable_balance_op should not be None.")
            return cls(type, create_claimable_balance_op=create_claimable_balance_op)
        if type == OperationType.CLAIM_CLAIMABLE_BALANCE:
            claim_claimable_balance_op = ClaimClaimableBalanceOp.unpack(unpacker)
            if claim_claimable_balance_op is None:
                raise ValueError("claim_claimable_balance_op should not be None.")
            return cls(type, claim_claimable_balance_op=claim_claimable_balance_op)
        if type == OperationType.BEGIN_SPONSORING_FUTURE_RESERVES:
            begin_sponsoring_future_reserves_op = (
                BeginSponsoringFutureReservesOp.unpack(unpacker)
            )
            if begin_sponsoring_future_reserves_op is None:
                raise ValueError(
                    "begin_sponsoring_future_reserves_op should not be None."
                )
            return cls(
                type,
                begin_sponsoring_future_reserves_op=begin_sponsoring_future_reserves_op,
            )
        if type == OperationType.END_SPONSORING_FUTURE_RESERVES:
            return cls(type)
        if type == OperationType.REVOKE_SPONSORSHIP:
            revoke_sponsorship_op = RevokeSponsorshipOp.unpack(unpacker)
            if revoke_sponsorship_op is None:
                raise ValueError("revoke_sponsorship_op should not be None.")
            return cls(type, revoke_sponsorship_op=revoke_sponsorship_op)
        if type == OperationType.CLAWBACK:
            clawback_op = ClawbackOp.unpack(unpacker)
            if clawback_op is None:
                raise ValueError("clawback_op should not be None.")
            return cls(type, clawback_op=clawback_op)
        if type == OperationType.CLAWBACK_CLAIMABLE_BALANCE:
            clawback_claimable_balance_op = ClawbackClaimableBalanceOp.unpack(unpacker)
            if clawback_claimable_balance_op is None:
                raise ValueError("clawback_claimable_balance_op should not be None.")
            return cls(
                type, clawback_claimable_balance_op=clawback_claimable_balance_op
            )
        if type == OperationType.SET_TRUST_LINE_FLAGS:
            set_trust_line_flags_op = SetTrustLineFlagsOp.unpack(unpacker)
            if set_trust_line_flags_op is None:
                raise ValueError("set_trust_line_flags_op should not be None.")
            return cls(type, set_trust_line_flags_op=set_trust_line_flags_op)
        return cls(type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "OperationBody":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "OperationBody":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.create_account_op == other.create_account_op
            and self.payment_op == other.payment_op
            and self.path_payment_strict_receive_op
            == other.path_payment_strict_receive_op
            and self.manage_sell_offer_op == other.manage_sell_offer_op
            and self.create_passive_sell_offer_op == other.create_passive_sell_offer_op
            and self.set_options_op == other.set_options_op
            and self.change_trust_op == other.change_trust_op
            and self.allow_trust_op == other.allow_trust_op
            and self.destination == other.destination
            and self.manage_data_op == other.manage_data_op
            and self.bump_sequence_op == other.bump_sequence_op
            and self.manage_buy_offer_op == other.manage_buy_offer_op
            and self.path_payment_strict_send_op == other.path_payment_strict_send_op
            and self.create_claimable_balance_op == other.create_claimable_balance_op
            and self.claim_claimable_balance_op == other.claim_claimable_balance_op
            and self.begin_sponsoring_future_reserves_op
            == other.begin_sponsoring_future_reserves_op
            and self.revoke_sponsorship_op == other.revoke_sponsorship_op
            and self.clawback_op == other.clawback_op
            and self.clawback_claimable_balance_op
            == other.clawback_claimable_balance_op
            and self.set_trust_line_flags_op == other.set_trust_line_flags_op
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(
            f"create_account_op={self.create_account_op}"
        ) if self.create_account_op is not None else None
        out.append(
            f"payment_op={self.payment_op}"
        ) if self.payment_op is not None else None
        out.append(
            f"path_payment_strict_receive_op={self.path_payment_strict_receive_op}"
        ) if self.path_payment_strict_receive_op is not None else None
        out.append(
            f"manage_sell_offer_op={self.manage_sell_offer_op}"
        ) if self.manage_sell_offer_op is not None else None
        out.append(
            f"create_passive_sell_offer_op={self.create_passive_sell_offer_op}"
        ) if self.create_passive_sell_offer_op is not None else None
        out.append(
            f"set_options_op={self.set_options_op}"
        ) if self.set_options_op is not None else None
        out.append(
            f"change_trust_op={self.change_trust_op}"
        ) if self.change_trust_op is not None else None
        out.append(
            f"allow_trust_op={self.allow_trust_op}"
        ) if self.allow_trust_op is not None else None
        out.append(
            f"destination={self.destination}"
        ) if self.destination is not None else None
        out.append(
            f"manage_data_op={self.manage_data_op}"
        ) if self.manage_data_op is not None else None
        out.append(
            f"bump_sequence_op={self.bump_sequence_op}"
        ) if self.bump_sequence_op is not None else None
        out.append(
            f"manage_buy_offer_op={self.manage_buy_offer_op}"
        ) if self.manage_buy_offer_op is not None else None
        out.append(
            f"path_payment_strict_send_op={self.path_payment_strict_send_op}"
        ) if self.path_payment_strict_send_op is not None else None
        out.append(
            f"create_claimable_balance_op={self.create_claimable_balance_op}"
        ) if self.create_claimable_balance_op is not None else None
        out.append(
            f"claim_claimable_balance_op={self.claim_claimable_balance_op}"
        ) if self.claim_claimable_balance_op is not None else None
        out.append(
            f"begin_sponsoring_future_reserves_op={self.begin_sponsoring_future_reserves_op}"
        ) if self.begin_sponsoring_future_reserves_op is not None else None
        out.append(
            f"revoke_sponsorship_op={self.revoke_sponsorship_op}"
        ) if self.revoke_sponsorship_op is not None else None
        out.append(
            f"clawback_op={self.clawback_op}"
        ) if self.clawback_op is not None else None
        out.append(
            f"clawback_claimable_balance_op={self.clawback_claimable_balance_op}"
        ) if self.clawback_claimable_balance_op is not None else None
        out.append(
            f"set_trust_line_flags_op={self.set_trust_line_flags_op}"
        ) if self.set_trust_line_flags_op is not None else None
        return f"<OperationBody {[', '.join(out)]}>"
