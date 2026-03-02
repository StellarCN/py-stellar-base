# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .muxed_account import MuxedAccount
from .operation_body import OperationBody

__all__ = ["Operation"]


class Operation:
    """
    XDR Source Code::

        struct Operation
        {
            // sourceAccount is the account used to run the operation
            // if not set, the runtime defaults to "sourceAccount" specified at
            // the transaction level
            MuxedAccount* sourceAccount;

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
            body;
        };
    """

    def __init__(
        self,
        source_account: Optional[MuxedAccount],
        body: OperationBody,
    ) -> None:
        self.source_account = source_account
        self.body = body

    def pack(self, packer: Packer) -> None:
        if self.source_account is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.source_account.pack(packer)
        self.body.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> Operation:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        source_account = (
            MuxedAccount.unpack(unpacker, depth_limit - 1)
            if unpacker.unpack_uint()
            else None
        )
        body = OperationBody.unpack(unpacker, depth_limit - 1)
        return cls(
            source_account=source_account,
            body=body,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Operation:
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
    def from_xdr(cls, xdr: str) -> Operation:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Operation:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "source_account": (
                self.source_account.to_json_dict()
                if self.source_account is not None
                else None
            ),
            "body": self.body.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> Operation:
        source_account = (
            MuxedAccount.from_json_dict(json_dict["source_account"])
            if json_dict["source_account"] is not None
            else None
        )
        body = OperationBody.from_json_dict(json_dict["body"])
        return cls(
            source_account=source_account,
            body=body,
        )

    def __hash__(self):
        return hash(
            (
                self.source_account,
                self.body,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.source_account == other.source_account and self.body == other.body

    def __repr__(self):
        out = [
            f"source_account={self.source_account}",
            f"body={self.body}",
        ]
        return f"<Operation [{', '.join(out)}]>"
