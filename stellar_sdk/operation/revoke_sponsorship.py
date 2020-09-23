import binascii
from enum import IntEnum

from .operation import Operation
from ..asset import Asset
from ..keypair import Keypair
from ..signer import Signer as XDRSigner
from ..xdr import Xdr


class RevokeSponsorshipType(IntEnum):
    ACCOUNT = 0
    TRUSTLINE = 1
    OFFER = 2
    DATA = 3
    CLAIMABLE_BALANCE = 4
    SIGNER = 5


class TrustLine:
    def __init__(self, account_id: str, asset: Asset):
        self.account_id = account_id
        self.asset = asset


class Offer:
    def __init__(self, seller_id: str, offer_id: int):
        self.seller_id = seller_id
        self.offer_id = offer_id


class Data:
    def __init__(self, account_id: str, data_name: str):
        self.account_id = account_id
        self.data_name = data_name


class Signer:
    def __init__(self, account_id: str, signer_key: XDRSigner):
        self.account_id = account_id
        self.signer_key = signer_key


class RevokeSponsorship(Operation):
    def __init__(self,
                 revoke_sponsorship_type: RevokeSponsorshipType,
                 account_id: str,
                 trustline: TrustLine,
                 offer: Offer,
                 data: Data,
                 claimable_balance_id: str,
                 signer: Signer,
                 source: str = None):
        super().__init__(source)
        self.revoke_sponsorship_type = revoke_sponsorship_type
        self.account_id = account_id
        self.trustline = trustline
        self.offer = offer
        self.data = data
        if isinstance(claimable_balance_id, str):
            claimable_balance_id = binascii.unhexlify(claimable_balance_id)
        self.claimable_balance_id: bytes = claimable_balance_id
        self.signer = signer

    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.REVOKE_SPONSORSHIP

    def _to_operation_body(self) -> Xdr.nullclass:
        body = Xdr.nullclass()
        body.type = Xdr.const.REVOKE_SPONSORSHIP
        if self.revoke_sponsorship_type == RevokeSponsorshipType.ACCOUNT:
            ledger_key = Xdr.nullclass()
            ledger_key.type = Xdr.const.ACCOUNT
            account = Xdr.nullclass()
            account.accountID = Keypair.from_public_key(self.account_id).xdr_account_id()
            ledger_key.account = account
            revoke_sponsorship_op = Xdr.nullclass()
            revoke_sponsorship_op.type = Xdr.const.REVOKE_SPONSORSHIP_LEDGER_ENTRY
            revoke_sponsorship_op.ledgerKey = ledger_key
            body.revokeSponsorshipOp = revoke_sponsorship_op
            return body
        elif self.revoke_sponsorship_type == RevokeSponsorshipType.TRUSTLINE:
            ledger_key = Xdr.nullclass()
            ledger_key.type = Xdr.const.TRUSTLINE
            trust_line = Xdr.nullclass()
            trust_line.accountID = Keypair.from_public_key(self.trustline.account_id).xdr_account_id()
            trust_line.asset = self.trustline.asset.to_xdr_object()
            ledger_key.trustLine = trust_line
            revoke_sponsorship_op = Xdr.nullclass()
            revoke_sponsorship_op.type = Xdr.const.REVOKE_SPONSORSHIP_LEDGER_ENTRY
            revoke_sponsorship_op.ledgerKey = ledger_key
            body.revokeSponsorshipOp = revoke_sponsorship_op
            return body
        elif self.revoke_sponsorship_type == RevokeSponsorshipType.OFFER:
            ledger_key = Xdr.nullclass()
            ledger_key.type = Xdr.const.OFFER
            offer = Xdr.nullclass()
            offer.sellerID = Keypair.from_public_key(self.offer.seller_id).xdr_account_id()
            offer.offerID = self.offer.offer_id
            ledger_key.offer = offer
            revoke_sponsorship_op = Xdr.nullclass()
            revoke_sponsorship_op.type = Xdr.const.REVOKE_SPONSORSHIP_LEDGER_ENTRY
            revoke_sponsorship_op.ledgerKey = ledger_key
            body.revokeSponsorshipOp = revoke_sponsorship_op
            return body
        elif self.revoke_sponsorship_type == RevokeSponsorshipType.DATA:
            ledger_key = Xdr.nullclass()
            ledger_key.type = Xdr.const.DATA
            data = Xdr.nullclass()
            data.accountID = Keypair.from_public_key(self.data.account_id).xdr_account_id()
            data.dataName = self.data.data_name
            ledger_key.account = data
            revoke_sponsorship_op = Xdr.nullclass()
            revoke_sponsorship_op.type = Xdr.const.REVOKE_SPONSORSHIP_LEDGER_ENTRY
            revoke_sponsorship_op.ledgerKey = ledger_key
            body.revokeSponsorshipOp = revoke_sponsorship_op
            return body
        elif self.revoke_sponsorship_type == RevokeSponsorshipType.CLAIMABLE_BALANCE:
            ledger_key = Xdr.nullclass()
            ledger_key.type = Xdr.const.CLAIMABLE_BALANCE
            claimable_balance = Xdr.nullclass()
            claimable_balance.accountID = Keypair.from_public_key(self.data.account_id).xdr_account_id()
            ledger_key.claimableBalance = claimable_balance
            revoke_sponsorship_op = Xdr.nullclass()
            revoke_sponsorship_op.type = Xdr.const.REVOKE_SPONSORSHIP_LEDGER_ENTRY
            revoke_sponsorship_op.ledgerKey = ledger_key
            body.revokeSponsorshipOp = revoke_sponsorship_op
            return body
        elif self.revoke_sponsorship_type == RevokeSponsorshipType.SIGNER:
            signer = Xdr.nullclass()
            signer.accountID = Keypair.from_public_key(self.signer.account_id).xdr_account_id()
            signer.signerKey = self.signer.signer_key.to_xdr_object()
            revoke_sponsorship_op = Xdr.nullclass()
            revoke_sponsorship_op.type = Xdr.const.REVOKE_SPONSORSHIP_SIGNER
            revoke_sponsorship_op.signer = signer
            body.revokeSponsorshipOp = revoke_sponsorship_op
        else:
            raise ValueError
