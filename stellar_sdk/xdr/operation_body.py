# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .allow_trust_op import AllowTrustOp
from .base import DEFAULT_XDR_MAX_DEPTH
from .begin_sponsoring_future_reserves_op import BeginSponsoringFutureReservesOp
from .bump_sequence_op import BumpSequenceOp
from .change_trust_op import ChangeTrustOp
from .claim_claimable_balance_op import ClaimClaimableBalanceOp
from .clawback_claimable_balance_op import ClawbackClaimableBalanceOp
from .clawback_op import ClawbackOp
from .create_account_op import CreateAccountOp
from .create_claimable_balance_op import CreateClaimableBalanceOp
from .create_passive_sell_offer_op import CreatePassiveSellOfferOp
from .extend_footprint_ttl_op import ExtendFootprintTTLOp
from .invoke_host_function_op import InvokeHostFunctionOp
from .liquidity_pool_deposit_op import LiquidityPoolDepositOp
from .liquidity_pool_withdraw_op import LiquidityPoolWithdrawOp
from .manage_buy_offer_op import ManageBuyOfferOp
from .manage_data_op import ManageDataOp
from .manage_sell_offer_op import ManageSellOfferOp
from .muxed_account import MuxedAccount
from .operation_type import OperationType
from .path_payment_strict_receive_op import PathPaymentStrictReceiveOp
from .path_payment_strict_send_op import PathPaymentStrictSendOp
from .payment_op import PaymentOp
from .restore_footprint_op import RestoreFootprintOp
from .revoke_sponsorship_op import RevokeSponsorshipOp
from .set_options_op import SetOptionsOp
from .set_trust_line_flags_op import SetTrustLineFlagsOp

__all__ = ["OperationBody"]


class OperationBody:
    """
    XDR Source Code::

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
            case LIQUIDITY_POOL_DEPOSIT:
                LiquidityPoolDepositOp liquidityPoolDepositOp;
            case LIQUIDITY_POOL_WITHDRAW:
                LiquidityPoolWithdrawOp liquidityPoolWithdrawOp;
            case INVOKE_HOST_FUNCTION:
                InvokeHostFunctionOp invokeHostFunctionOp;
            case EXTEND_FOOTPRINT_TTL:
                ExtendFootprintTTLOp extendFootprintTTLOp;
            case RESTORE_FOOTPRINT:
                RestoreFootprintOp restoreFootprintOp;
            }
    """

    def __init__(
        self,
        type: OperationType,
        create_account_op: Optional[CreateAccountOp] = None,
        payment_op: Optional[PaymentOp] = None,
        path_payment_strict_receive_op: Optional[PathPaymentStrictReceiveOp] = None,
        manage_sell_offer_op: Optional[ManageSellOfferOp] = None,
        create_passive_sell_offer_op: Optional[CreatePassiveSellOfferOp] = None,
        set_options_op: Optional[SetOptionsOp] = None,
        change_trust_op: Optional[ChangeTrustOp] = None,
        allow_trust_op: Optional[AllowTrustOp] = None,
        destination: Optional[MuxedAccount] = None,
        manage_data_op: Optional[ManageDataOp] = None,
        bump_sequence_op: Optional[BumpSequenceOp] = None,
        manage_buy_offer_op: Optional[ManageBuyOfferOp] = None,
        path_payment_strict_send_op: Optional[PathPaymentStrictSendOp] = None,
        create_claimable_balance_op: Optional[CreateClaimableBalanceOp] = None,
        claim_claimable_balance_op: Optional[ClaimClaimableBalanceOp] = None,
        begin_sponsoring_future_reserves_op: Optional[
            BeginSponsoringFutureReservesOp
        ] = None,
        revoke_sponsorship_op: Optional[RevokeSponsorshipOp] = None,
        clawback_op: Optional[ClawbackOp] = None,
        clawback_claimable_balance_op: Optional[ClawbackClaimableBalanceOp] = None,
        set_trust_line_flags_op: Optional[SetTrustLineFlagsOp] = None,
        liquidity_pool_deposit_op: Optional[LiquidityPoolDepositOp] = None,
        liquidity_pool_withdraw_op: Optional[LiquidityPoolWithdrawOp] = None,
        invoke_host_function_op: Optional[InvokeHostFunctionOp] = None,
        extend_footprint_ttl_op: Optional[ExtendFootprintTTLOp] = None,
        restore_footprint_op: Optional[RestoreFootprintOp] = None,
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
        self.liquidity_pool_deposit_op = liquidity_pool_deposit_op
        self.liquidity_pool_withdraw_op = liquidity_pool_withdraw_op
        self.invoke_host_function_op = invoke_host_function_op
        self.extend_footprint_ttl_op = extend_footprint_ttl_op
        self.restore_footprint_op = restore_footprint_op

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
        if self.type == OperationType.LIQUIDITY_POOL_DEPOSIT:
            if self.liquidity_pool_deposit_op is None:
                raise ValueError("liquidity_pool_deposit_op should not be None.")
            self.liquidity_pool_deposit_op.pack(packer)
            return
        if self.type == OperationType.LIQUIDITY_POOL_WITHDRAW:
            if self.liquidity_pool_withdraw_op is None:
                raise ValueError("liquidity_pool_withdraw_op should not be None.")
            self.liquidity_pool_withdraw_op.pack(packer)
            return
        if self.type == OperationType.INVOKE_HOST_FUNCTION:
            if self.invoke_host_function_op is None:
                raise ValueError("invoke_host_function_op should not be None.")
            self.invoke_host_function_op.pack(packer)
            return
        if self.type == OperationType.EXTEND_FOOTPRINT_TTL:
            if self.extend_footprint_ttl_op is None:
                raise ValueError("extend_footprint_ttl_op should not be None.")
            self.extend_footprint_ttl_op.pack(packer)
            return
        if self.type == OperationType.RESTORE_FOOTPRINT:
            if self.restore_footprint_op is None:
                raise ValueError("restore_footprint_op should not be None.")
            self.restore_footprint_op.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> OperationBody:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = OperationType.unpack(unpacker)
        if type == OperationType.CREATE_ACCOUNT:
            create_account_op = CreateAccountOp.unpack(unpacker, depth_limit - 1)
            return cls(type=type, create_account_op=create_account_op)
        if type == OperationType.PAYMENT:
            payment_op = PaymentOp.unpack(unpacker, depth_limit - 1)
            return cls(type=type, payment_op=payment_op)
        if type == OperationType.PATH_PAYMENT_STRICT_RECEIVE:
            path_payment_strict_receive_op = PathPaymentStrictReceiveOp.unpack(
                unpacker, depth_limit - 1
            )
            return cls(
                type=type, path_payment_strict_receive_op=path_payment_strict_receive_op
            )
        if type == OperationType.MANAGE_SELL_OFFER:
            manage_sell_offer_op = ManageSellOfferOp.unpack(unpacker, depth_limit - 1)
            return cls(type=type, manage_sell_offer_op=manage_sell_offer_op)
        if type == OperationType.CREATE_PASSIVE_SELL_OFFER:
            create_passive_sell_offer_op = CreatePassiveSellOfferOp.unpack(
                unpacker, depth_limit - 1
            )
            return cls(
                type=type, create_passive_sell_offer_op=create_passive_sell_offer_op
            )
        if type == OperationType.SET_OPTIONS:
            set_options_op = SetOptionsOp.unpack(unpacker, depth_limit - 1)
            return cls(type=type, set_options_op=set_options_op)
        if type == OperationType.CHANGE_TRUST:
            change_trust_op = ChangeTrustOp.unpack(unpacker, depth_limit - 1)
            return cls(type=type, change_trust_op=change_trust_op)
        if type == OperationType.ALLOW_TRUST:
            allow_trust_op = AllowTrustOp.unpack(unpacker, depth_limit - 1)
            return cls(type=type, allow_trust_op=allow_trust_op)
        if type == OperationType.ACCOUNT_MERGE:
            destination = MuxedAccount.unpack(unpacker, depth_limit - 1)
            return cls(type=type, destination=destination)
        if type == OperationType.INFLATION:
            return cls(type=type)
        if type == OperationType.MANAGE_DATA:
            manage_data_op = ManageDataOp.unpack(unpacker, depth_limit - 1)
            return cls(type=type, manage_data_op=manage_data_op)
        if type == OperationType.BUMP_SEQUENCE:
            bump_sequence_op = BumpSequenceOp.unpack(unpacker, depth_limit - 1)
            return cls(type=type, bump_sequence_op=bump_sequence_op)
        if type == OperationType.MANAGE_BUY_OFFER:
            manage_buy_offer_op = ManageBuyOfferOp.unpack(unpacker, depth_limit - 1)
            return cls(type=type, manage_buy_offer_op=manage_buy_offer_op)
        if type == OperationType.PATH_PAYMENT_STRICT_SEND:
            path_payment_strict_send_op = PathPaymentStrictSendOp.unpack(
                unpacker, depth_limit - 1
            )
            return cls(
                type=type, path_payment_strict_send_op=path_payment_strict_send_op
            )
        if type == OperationType.CREATE_CLAIMABLE_BALANCE:
            create_claimable_balance_op = CreateClaimableBalanceOp.unpack(
                unpacker, depth_limit - 1
            )
            return cls(
                type=type, create_claimable_balance_op=create_claimable_balance_op
            )
        if type == OperationType.CLAIM_CLAIMABLE_BALANCE:
            claim_claimable_balance_op = ClaimClaimableBalanceOp.unpack(
                unpacker, depth_limit - 1
            )
            return cls(type=type, claim_claimable_balance_op=claim_claimable_balance_op)
        if type == OperationType.BEGIN_SPONSORING_FUTURE_RESERVES:
            begin_sponsoring_future_reserves_op = (
                BeginSponsoringFutureReservesOp.unpack(unpacker, depth_limit - 1)
            )
            return cls(
                type=type,
                begin_sponsoring_future_reserves_op=begin_sponsoring_future_reserves_op,
            )
        if type == OperationType.END_SPONSORING_FUTURE_RESERVES:
            return cls(type=type)
        if type == OperationType.REVOKE_SPONSORSHIP:
            revoke_sponsorship_op = RevokeSponsorshipOp.unpack(
                unpacker, depth_limit - 1
            )
            return cls(type=type, revoke_sponsorship_op=revoke_sponsorship_op)
        if type == OperationType.CLAWBACK:
            clawback_op = ClawbackOp.unpack(unpacker, depth_limit - 1)
            return cls(type=type, clawback_op=clawback_op)
        if type == OperationType.CLAWBACK_CLAIMABLE_BALANCE:
            clawback_claimable_balance_op = ClawbackClaimableBalanceOp.unpack(
                unpacker, depth_limit - 1
            )
            return cls(
                type=type, clawback_claimable_balance_op=clawback_claimable_balance_op
            )
        if type == OperationType.SET_TRUST_LINE_FLAGS:
            set_trust_line_flags_op = SetTrustLineFlagsOp.unpack(
                unpacker, depth_limit - 1
            )
            return cls(type=type, set_trust_line_flags_op=set_trust_line_flags_op)
        if type == OperationType.LIQUIDITY_POOL_DEPOSIT:
            liquidity_pool_deposit_op = LiquidityPoolDepositOp.unpack(
                unpacker, depth_limit - 1
            )
            return cls(type=type, liquidity_pool_deposit_op=liquidity_pool_deposit_op)
        if type == OperationType.LIQUIDITY_POOL_WITHDRAW:
            liquidity_pool_withdraw_op = LiquidityPoolWithdrawOp.unpack(
                unpacker, depth_limit - 1
            )
            return cls(type=type, liquidity_pool_withdraw_op=liquidity_pool_withdraw_op)
        if type == OperationType.INVOKE_HOST_FUNCTION:
            invoke_host_function_op = InvokeHostFunctionOp.unpack(
                unpacker, depth_limit - 1
            )
            return cls(type=type, invoke_host_function_op=invoke_host_function_op)
        if type == OperationType.EXTEND_FOOTPRINT_TTL:
            extend_footprint_ttl_op = ExtendFootprintTTLOp.unpack(
                unpacker, depth_limit - 1
            )
            return cls(type=type, extend_footprint_ttl_op=extend_footprint_ttl_op)
        if type == OperationType.RESTORE_FOOTPRINT:
            restore_footprint_op = RestoreFootprintOp.unpack(unpacker, depth_limit - 1)
            return cls(type=type, restore_footprint_op=restore_footprint_op)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> OperationBody:
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
    def from_xdr(cls, xdr: str) -> OperationBody:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> OperationBody:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.type == OperationType.CREATE_ACCOUNT:
            assert self.create_account_op is not None
            return {"create_account": self.create_account_op.to_json_dict()}
        if self.type == OperationType.PAYMENT:
            assert self.payment_op is not None
            return {"payment": self.payment_op.to_json_dict()}
        if self.type == OperationType.PATH_PAYMENT_STRICT_RECEIVE:
            assert self.path_payment_strict_receive_op is not None
            return {
                "path_payment_strict_receive": self.path_payment_strict_receive_op.to_json_dict()
            }
        if self.type == OperationType.MANAGE_SELL_OFFER:
            assert self.manage_sell_offer_op is not None
            return {"manage_sell_offer": self.manage_sell_offer_op.to_json_dict()}
        if self.type == OperationType.CREATE_PASSIVE_SELL_OFFER:
            assert self.create_passive_sell_offer_op is not None
            return {
                "create_passive_sell_offer": self.create_passive_sell_offer_op.to_json_dict()
            }
        if self.type == OperationType.SET_OPTIONS:
            assert self.set_options_op is not None
            return {"set_options": self.set_options_op.to_json_dict()}
        if self.type == OperationType.CHANGE_TRUST:
            assert self.change_trust_op is not None
            return {"change_trust": self.change_trust_op.to_json_dict()}
        if self.type == OperationType.ALLOW_TRUST:
            assert self.allow_trust_op is not None
            return {"allow_trust": self.allow_trust_op.to_json_dict()}
        if self.type == OperationType.ACCOUNT_MERGE:
            assert self.destination is not None
            return {"account_merge": self.destination.to_json_dict()}
        if self.type == OperationType.INFLATION:
            return "inflation"
        if self.type == OperationType.MANAGE_DATA:
            assert self.manage_data_op is not None
            return {"manage_data": self.manage_data_op.to_json_dict()}
        if self.type == OperationType.BUMP_SEQUENCE:
            assert self.bump_sequence_op is not None
            return {"bump_sequence": self.bump_sequence_op.to_json_dict()}
        if self.type == OperationType.MANAGE_BUY_OFFER:
            assert self.manage_buy_offer_op is not None
            return {"manage_buy_offer": self.manage_buy_offer_op.to_json_dict()}
        if self.type == OperationType.PATH_PAYMENT_STRICT_SEND:
            assert self.path_payment_strict_send_op is not None
            return {
                "path_payment_strict_send": self.path_payment_strict_send_op.to_json_dict()
            }
        if self.type == OperationType.CREATE_CLAIMABLE_BALANCE:
            assert self.create_claimable_balance_op is not None
            return {
                "create_claimable_balance": self.create_claimable_balance_op.to_json_dict()
            }
        if self.type == OperationType.CLAIM_CLAIMABLE_BALANCE:
            assert self.claim_claimable_balance_op is not None
            return {
                "claim_claimable_balance": self.claim_claimable_balance_op.to_json_dict()
            }
        if self.type == OperationType.BEGIN_SPONSORING_FUTURE_RESERVES:
            assert self.begin_sponsoring_future_reserves_op is not None
            return {
                "begin_sponsoring_future_reserves": self.begin_sponsoring_future_reserves_op.to_json_dict()
            }
        if self.type == OperationType.END_SPONSORING_FUTURE_RESERVES:
            return "end_sponsoring_future_reserves"
        if self.type == OperationType.REVOKE_SPONSORSHIP:
            assert self.revoke_sponsorship_op is not None
            return {"revoke_sponsorship": self.revoke_sponsorship_op.to_json_dict()}
        if self.type == OperationType.CLAWBACK:
            assert self.clawback_op is not None
            return {"clawback": self.clawback_op.to_json_dict()}
        if self.type == OperationType.CLAWBACK_CLAIMABLE_BALANCE:
            assert self.clawback_claimable_balance_op is not None
            return {
                "clawback_claimable_balance": self.clawback_claimable_balance_op.to_json_dict()
            }
        if self.type == OperationType.SET_TRUST_LINE_FLAGS:
            assert self.set_trust_line_flags_op is not None
            return {"set_trust_line_flags": self.set_trust_line_flags_op.to_json_dict()}
        if self.type == OperationType.LIQUIDITY_POOL_DEPOSIT:
            assert self.liquidity_pool_deposit_op is not None
            return {
                "liquidity_pool_deposit": self.liquidity_pool_deposit_op.to_json_dict()
            }
        if self.type == OperationType.LIQUIDITY_POOL_WITHDRAW:
            assert self.liquidity_pool_withdraw_op is not None
            return {
                "liquidity_pool_withdraw": self.liquidity_pool_withdraw_op.to_json_dict()
            }
        if self.type == OperationType.INVOKE_HOST_FUNCTION:
            assert self.invoke_host_function_op is not None
            return {"invoke_host_function": self.invoke_host_function_op.to_json_dict()}
        if self.type == OperationType.EXTEND_FOOTPRINT_TTL:
            assert self.extend_footprint_ttl_op is not None
            return {"extend_footprint_ttl": self.extend_footprint_ttl_op.to_json_dict()}
        if self.type == OperationType.RESTORE_FOOTPRINT:
            assert self.restore_footprint_op is not None
            return {"restore_footprint": self.restore_footprint_op.to_json_dict()}
        raise ValueError(f"Unknown type in OperationBody: {self.type}")

    @classmethod
    def from_json_dict(cls, json_value: str | dict) -> OperationBody:
        if isinstance(json_value, str):
            if json_value not in (
                "inflation",
                "end_sponsoring_future_reserves",
            ):
                raise ValueError(
                    f"Unexpected string '{json_value}' for OperationBody, must be one of: inflation, end_sponsoring_future_reserves"
                )
            type = OperationType.from_json_dict(json_value)
            return cls(type=type)
        if not isinstance(json_value, dict) or len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for OperationBody, got: {json_value}"
            )
        key = next(iter(json_value))
        type = OperationType.from_json_dict(key)
        if key == "create_account":
            create_account_op = CreateAccountOp.from_json_dict(
                json_value["create_account"]
            )
            return cls(type=type, create_account_op=create_account_op)
        if key == "payment":
            payment_op = PaymentOp.from_json_dict(json_value["payment"])
            return cls(type=type, payment_op=payment_op)
        if key == "path_payment_strict_receive":
            path_payment_strict_receive_op = PathPaymentStrictReceiveOp.from_json_dict(
                json_value["path_payment_strict_receive"]
            )
            return cls(
                type=type, path_payment_strict_receive_op=path_payment_strict_receive_op
            )
        if key == "manage_sell_offer":
            manage_sell_offer_op = ManageSellOfferOp.from_json_dict(
                json_value["manage_sell_offer"]
            )
            return cls(type=type, manage_sell_offer_op=manage_sell_offer_op)
        if key == "create_passive_sell_offer":
            create_passive_sell_offer_op = CreatePassiveSellOfferOp.from_json_dict(
                json_value["create_passive_sell_offer"]
            )
            return cls(
                type=type, create_passive_sell_offer_op=create_passive_sell_offer_op
            )
        if key == "set_options":
            set_options_op = SetOptionsOp.from_json_dict(json_value["set_options"])
            return cls(type=type, set_options_op=set_options_op)
        if key == "change_trust":
            change_trust_op = ChangeTrustOp.from_json_dict(json_value["change_trust"])
            return cls(type=type, change_trust_op=change_trust_op)
        if key == "allow_trust":
            allow_trust_op = AllowTrustOp.from_json_dict(json_value["allow_trust"])
            return cls(type=type, allow_trust_op=allow_trust_op)
        if key == "account_merge":
            destination = MuxedAccount.from_json_dict(json_value["account_merge"])
            return cls(type=type, destination=destination)
        if key == "manage_data":
            manage_data_op = ManageDataOp.from_json_dict(json_value["manage_data"])
            return cls(type=type, manage_data_op=manage_data_op)
        if key == "bump_sequence":
            bump_sequence_op = BumpSequenceOp.from_json_dict(
                json_value["bump_sequence"]
            )
            return cls(type=type, bump_sequence_op=bump_sequence_op)
        if key == "manage_buy_offer":
            manage_buy_offer_op = ManageBuyOfferOp.from_json_dict(
                json_value["manage_buy_offer"]
            )
            return cls(type=type, manage_buy_offer_op=manage_buy_offer_op)
        if key == "path_payment_strict_send":
            path_payment_strict_send_op = PathPaymentStrictSendOp.from_json_dict(
                json_value["path_payment_strict_send"]
            )
            return cls(
                type=type, path_payment_strict_send_op=path_payment_strict_send_op
            )
        if key == "create_claimable_balance":
            create_claimable_balance_op = CreateClaimableBalanceOp.from_json_dict(
                json_value["create_claimable_balance"]
            )
            return cls(
                type=type, create_claimable_balance_op=create_claimable_balance_op
            )
        if key == "claim_claimable_balance":
            claim_claimable_balance_op = ClaimClaimableBalanceOp.from_json_dict(
                json_value["claim_claimable_balance"]
            )
            return cls(type=type, claim_claimable_balance_op=claim_claimable_balance_op)
        if key == "begin_sponsoring_future_reserves":
            begin_sponsoring_future_reserves_op = (
                BeginSponsoringFutureReservesOp.from_json_dict(
                    json_value["begin_sponsoring_future_reserves"]
                )
            )
            return cls(
                type=type,
                begin_sponsoring_future_reserves_op=begin_sponsoring_future_reserves_op,
            )
        if key == "revoke_sponsorship":
            revoke_sponsorship_op = RevokeSponsorshipOp.from_json_dict(
                json_value["revoke_sponsorship"]
            )
            return cls(type=type, revoke_sponsorship_op=revoke_sponsorship_op)
        if key == "clawback":
            clawback_op = ClawbackOp.from_json_dict(json_value["clawback"])
            return cls(type=type, clawback_op=clawback_op)
        if key == "clawback_claimable_balance":
            clawback_claimable_balance_op = ClawbackClaimableBalanceOp.from_json_dict(
                json_value["clawback_claimable_balance"]
            )
            return cls(
                type=type, clawback_claimable_balance_op=clawback_claimable_balance_op
            )
        if key == "set_trust_line_flags":
            set_trust_line_flags_op = SetTrustLineFlagsOp.from_json_dict(
                json_value["set_trust_line_flags"]
            )
            return cls(type=type, set_trust_line_flags_op=set_trust_line_flags_op)
        if key == "liquidity_pool_deposit":
            liquidity_pool_deposit_op = LiquidityPoolDepositOp.from_json_dict(
                json_value["liquidity_pool_deposit"]
            )
            return cls(type=type, liquidity_pool_deposit_op=liquidity_pool_deposit_op)
        if key == "liquidity_pool_withdraw":
            liquidity_pool_withdraw_op = LiquidityPoolWithdrawOp.from_json_dict(
                json_value["liquidity_pool_withdraw"]
            )
            return cls(type=type, liquidity_pool_withdraw_op=liquidity_pool_withdraw_op)
        if key == "invoke_host_function":
            invoke_host_function_op = InvokeHostFunctionOp.from_json_dict(
                json_value["invoke_host_function"]
            )
            return cls(type=type, invoke_host_function_op=invoke_host_function_op)
        if key == "extend_footprint_ttl":
            extend_footprint_ttl_op = ExtendFootprintTTLOp.from_json_dict(
                json_value["extend_footprint_ttl"]
            )
            return cls(type=type, extend_footprint_ttl_op=extend_footprint_ttl_op)
        if key == "restore_footprint":
            restore_footprint_op = RestoreFootprintOp.from_json_dict(
                json_value["restore_footprint"]
            )
            return cls(type=type, restore_footprint_op=restore_footprint_op)
        raise ValueError(f"Unknown key '{key}' for OperationBody")

    def __hash__(self):
        return hash(
            (
                self.type,
                self.create_account_op,
                self.payment_op,
                self.path_payment_strict_receive_op,
                self.manage_sell_offer_op,
                self.create_passive_sell_offer_op,
                self.set_options_op,
                self.change_trust_op,
                self.allow_trust_op,
                self.destination,
                self.manage_data_op,
                self.bump_sequence_op,
                self.manage_buy_offer_op,
                self.path_payment_strict_send_op,
                self.create_claimable_balance_op,
                self.claim_claimable_balance_op,
                self.begin_sponsoring_future_reserves_op,
                self.revoke_sponsorship_op,
                self.clawback_op,
                self.clawback_claimable_balance_op,
                self.set_trust_line_flags_op,
                self.liquidity_pool_deposit_op,
                self.liquidity_pool_withdraw_op,
                self.invoke_host_function_op,
                self.extend_footprint_ttl_op,
                self.restore_footprint_op,
            )
        )

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
            and self.liquidity_pool_deposit_op == other.liquidity_pool_deposit_op
            and self.liquidity_pool_withdraw_op == other.liquidity_pool_withdraw_op
            and self.invoke_host_function_op == other.invoke_host_function_op
            and self.extend_footprint_ttl_op == other.extend_footprint_ttl_op
            and self.restore_footprint_op == other.restore_footprint_op
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        if self.create_account_op is not None:
            out.append(f"create_account_op={self.create_account_op}")
        if self.payment_op is not None:
            out.append(f"payment_op={self.payment_op}")
        if self.path_payment_strict_receive_op is not None:
            out.append(
                f"path_payment_strict_receive_op={self.path_payment_strict_receive_op}"
            )
        if self.manage_sell_offer_op is not None:
            out.append(f"manage_sell_offer_op={self.manage_sell_offer_op}")
        if self.create_passive_sell_offer_op is not None:
            out.append(
                f"create_passive_sell_offer_op={self.create_passive_sell_offer_op}"
            )
        if self.set_options_op is not None:
            out.append(f"set_options_op={self.set_options_op}")
        if self.change_trust_op is not None:
            out.append(f"change_trust_op={self.change_trust_op}")
        if self.allow_trust_op is not None:
            out.append(f"allow_trust_op={self.allow_trust_op}")
        if self.destination is not None:
            out.append(f"destination={self.destination}")
        if self.manage_data_op is not None:
            out.append(f"manage_data_op={self.manage_data_op}")
        if self.bump_sequence_op is not None:
            out.append(f"bump_sequence_op={self.bump_sequence_op}")
        if self.manage_buy_offer_op is not None:
            out.append(f"manage_buy_offer_op={self.manage_buy_offer_op}")
        if self.path_payment_strict_send_op is not None:
            out.append(
                f"path_payment_strict_send_op={self.path_payment_strict_send_op}"
            )
        if self.create_claimable_balance_op is not None:
            out.append(
                f"create_claimable_balance_op={self.create_claimable_balance_op}"
            )
        if self.claim_claimable_balance_op is not None:
            out.append(f"claim_claimable_balance_op={self.claim_claimable_balance_op}")
        if self.begin_sponsoring_future_reserves_op is not None:
            out.append(
                f"begin_sponsoring_future_reserves_op={self.begin_sponsoring_future_reserves_op}"
            )
        if self.revoke_sponsorship_op is not None:
            out.append(f"revoke_sponsorship_op={self.revoke_sponsorship_op}")
        if self.clawback_op is not None:
            out.append(f"clawback_op={self.clawback_op}")
        if self.clawback_claimable_balance_op is not None:
            out.append(
                f"clawback_claimable_balance_op={self.clawback_claimable_balance_op}"
            )
        if self.set_trust_line_flags_op is not None:
            out.append(f"set_trust_line_flags_op={self.set_trust_line_flags_op}")
        if self.liquidity_pool_deposit_op is not None:
            out.append(f"liquidity_pool_deposit_op={self.liquidity_pool_deposit_op}")
        if self.liquidity_pool_withdraw_op is not None:
            out.append(f"liquidity_pool_withdraw_op={self.liquidity_pool_withdraw_op}")
        if self.invoke_host_function_op is not None:
            out.append(f"invoke_host_function_op={self.invoke_host_function_op}")
        if self.extend_footprint_ttl_op is not None:
            out.append(f"extend_footprint_ttl_op={self.extend_footprint_ttl_op}")
        if self.restore_footprint_op is not None:
            out.append(f"restore_footprint_op={self.restore_footprint_op}")
        return f"<OperationBody [{', '.join(out)}]>"
