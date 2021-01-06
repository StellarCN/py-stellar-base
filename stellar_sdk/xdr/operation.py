# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import Optional
from xdrlib import Packer, Unpacker

from .muxed_account import MuxedAccount
from .operation_body import OperationBody

__all__ = ["Operation"]


class Operation:
    """
    XDR Source Code
    ----------------------------------------------------------------
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
        }
        body;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self, source_account: Optional[MuxedAccount], body: OperationBody,
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
    def unpack(cls, unpacker: Unpacker) -> "Operation":
        source_account = (
            MuxedAccount.unpack(unpacker) if unpacker.unpack_uint() else None
        )
        body = OperationBody.unpack(unpacker)
        return cls(source_account=source_account, body=body,)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "Operation":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Operation":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.source_account == other.source_account and self.body == other.body

    def __str__(self):
        out = [
            f"source_account={self.source_account}",
            f"body={self.body}",
        ]
        return f"<Operation {[', '.join(out)]}>"
