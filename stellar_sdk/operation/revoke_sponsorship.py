import binascii
from enum import IntEnum
from typing import Optional

from .operation import Operation
from ..asset import Asset
from ..keypair import Keypair
from ..signer_key import SignerKey
from ..strkey import StrKey
from ..xdr import Xdr
from ..exceptions import ValueError
from .utils import check_ed25519_public_key


class RevokeSponsorshipType(IntEnum):
    """Currently supported RevokeSponsorship types.
    """

    ACCOUNT = 0
    TRUSTLINE = 1
    OFFER = 2
    DATA = 3
    CLAIMABLE_BALANCE = 4
    SIGNER = 5


class TrustLine:
    def __init__(self, account_id: str, asset: Asset) -> None:
        check_ed25519_public_key(account_id)
        self.account_id = account_id
        self.asset = asset


class Offer:
    def __init__(self, seller_id: str, offer_id: int) -> None:
        check_ed25519_public_key(seller_id)
        self.seller_id = seller_id
        self.offer_id = offer_id


class Data:
    def __init__(self, account_id: str, data_name: str) -> None:
        check_ed25519_public_key(account_id)
        self.account_id = account_id
        self.data_name = data_name


class Signer:
    def __init__(self, account_id: str, signer_key: SignerKey) -> None:
        check_ed25519_public_key(account_id)
        self.account_id = account_id
        self.signer_key = signer_key


class RevokeSponsorship(Operation):
    """

    """

    def __init__(
        self,
        revoke_sponsorship_type: RevokeSponsorshipType,
        account_id: Optional[str],
        trustline: Optional[TrustLine],
        offer: Optional[Offer],
        data: Optional[Data],
        claimable_balance_id: Optional[str],
        signer: Optional[Signer],
        source: str = None,
    ) -> None:
        super().__init__(source)
        self.revoke_sponsorship_type = revoke_sponsorship_type
        self.account_id = account_id
        self.trustline = trustline
        self.offer = offer
        self.data = data
        self.claimable_balance_id = claimable_balance_id
        self.signer = signer

    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.REVOKE_SPONSORSHIP

    @classmethod
    def revoke_account_sponsorship(cls, account_id: str, source: str = None):
        """Create a "revoke sponsorship" operation for an account.

        :param account_id: The sponsored account ID.
        :param source: The source account (defaults to transaction source).
        :return: A "revoke sponsorship" operation for an account.
        """
        return cls(
            revoke_sponsorship_type=RevokeSponsorshipType.ACCOUNT,
            account_id=account_id,
            trustline=None,
            offer=None,
            data=None,
            claimable_balance_id=None,
            signer=None,
            source=source,
        )

    @classmethod
    def revoke_trustline_sponsorship(
        cls, account_id: str, asset: Asset, source: str = None
    ):
        """Create a "revoke sponsorship" operation for a trustline.

        :param account_id: The account ID which owns the trustline.
        :param asset: The asset in the trustline.
        :param source: The source account (defaults to transaction source).
        :return: A "revoke sponsorship" operation for a trustline.
        """
        trustline = TrustLine(account_id=account_id, asset=asset)
        return cls(
            revoke_sponsorship_type=RevokeSponsorshipType.TRUSTLINE,
            account_id=None,
            trustline=trustline,
            offer=None,
            data=None,
            claimable_balance_id=None,
            signer=None,
            source=source,
        )

    @classmethod
    def revoke_offer_sponsorship(
        cls, seller_id: str, offer_id: int, source: str = None
    ):
        """Create a "revoke sponsorship" operation for an offer.

        :param seller_id: The account ID which created the offer.
        :param offer_id: The offer ID.
        :param source: The source account (defaults to transaction source).
        :return: A "revoke sponsorship" operation for an offer.
        """
        offer = Offer(seller_id=seller_id, offer_id=offer_id)
        return cls(
            revoke_sponsorship_type=RevokeSponsorshipType.OFFER,
            account_id=None,
            trustline=None,
            offer=offer,
            data=None,
            claimable_balance_id=None,
            signer=None,
            source=source,
        )

    @classmethod
    def revoke_data_sponsorship(
        cls, account_id: str, data_name: str, source: str = None
    ):
        """Create a "revoke sponsorship" operation for a data entry.

        :param account_id: The account ID which owns the data entry.
        :param data_name: The name of the data entry
        :param source: The source account (defaults to transaction source).
        :return: A "revoke sponsorship" operation for a data entry.
        """
        data = Data(account_id=account_id, data_name=data_name)
        return cls(
            revoke_sponsorship_type=RevokeSponsorshipType.DATA,
            account_id=None,
            trustline=None,
            offer=None,
            data=data,
            claimable_balance_id=None,
            signer=None,
            source=source,
        )

    @classmethod
    def revoke_claimable_balance_sponsorship(
        cls, claimable_balance_id: str, source: str = None
    ):
        """Create a "revoke sponsorship" operation for a claimable balance.

        :param claimable_balance_id: The sponsored claimable balance ID.
        :param source: The source account (defaults to transaction source).
        :return: A "revoke sponsorship" operation for a claimable balance.
        """
        return cls(
            revoke_sponsorship_type=RevokeSponsorshipType.CLAIMABLE_BALANCE,
            account_id=None,
            trustline=None,
            offer=None,
            data=None,
            claimable_balance_id=claimable_balance_id,
            signer=None,
            source=source,
        )

    @classmethod
    def revoke_signer_sponsorship(
        cls, account_id: str, signer_key: SignerKey, source: str = None
    ):
        """Create a "revoke sponsorship" operation for a signer.

        :param account_id: The account ID where the signer sponsorship is being removed from.
        :param signer_key: The signer whose sponsorship is being removed.
        :param source: The source account (defaults to transaction source).
        :return: A "revoke sponsorship" operation for a signer.
        """
        signer = Signer(account_id=account_id, signer_key=signer_key)
        return cls(
            revoke_sponsorship_type=RevokeSponsorshipType.SIGNER,
            account_id=None,
            trustline=None,
            offer=None,
            data=None,
            claimable_balance_id=None,
            signer=signer,
            source=source,
        )

    def _to_operation_body(self) -> Xdr.nullclass:
        body = Xdr.nullclass()
        body.type = Xdr.const.REVOKE_SPONSORSHIP
        if self.revoke_sponsorship_type == RevokeSponsorshipType.ACCOUNT:
            ledger_key = Xdr.nullclass()
            ledger_key.type = Xdr.const.ACCOUNT
            account = Xdr.nullclass()
            account.accountID = Keypair.from_public_key(
                self.account_id
            ).xdr_account_id()
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
            trust_line.accountID = Keypair.from_public_key(
                self.trustline.account_id
            ).xdr_account_id()
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
            offer.sellerID = Keypair.from_public_key(
                self.offer.seller_id
            ).xdr_account_id()
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
            data.accountID = Keypair.from_public_key(
                self.data.account_id
            ).xdr_account_id()
            data.dataName = self.data.data_name.encode()
            ledger_key.data = data
            revoke_sponsorship_op = Xdr.nullclass()
            revoke_sponsorship_op.type = Xdr.const.REVOKE_SPONSORSHIP_LEDGER_ENTRY
            revoke_sponsorship_op.ledgerKey = ledger_key
            body.revokeSponsorshipOp = revoke_sponsorship_op
            return body
        elif self.revoke_sponsorship_type == RevokeSponsorshipType.CLAIMABLE_BALANCE:
            ledger_key = Xdr.nullclass()
            ledger_key.type = Xdr.const.CLAIMABLE_BALANCE
            claimable_balance_bytes = binascii.unhexlify(self.claimable_balance_id)
            claimable_balance = Xdr.nullclass()
            balance_id = Xdr.nullclass()
            balance_id.type = Xdr.const.CLAIMABLE_BALANCE_ID_TYPE_V0  # int32
            balance_id.v0 = claimable_balance_bytes[4:]
            claimable_balance.balanceID = balance_id
            ledger_key.claimableBalance = claimable_balance
            revoke_sponsorship_op = Xdr.nullclass()
            revoke_sponsorship_op.type = Xdr.const.REVOKE_SPONSORSHIP_LEDGER_ENTRY
            revoke_sponsorship_op.ledgerKey = ledger_key
            body.revokeSponsorshipOp = revoke_sponsorship_op
            return body
        elif self.revoke_sponsorship_type == RevokeSponsorshipType.SIGNER:
            signer = Xdr.nullclass()
            signer.accountID = Keypair.from_public_key(
                self.signer.account_id
            ).xdr_account_id()
            signer.signerKey = self.signer.signer_key.to_xdr_object()
            revoke_sponsorship_op = Xdr.nullclass()
            revoke_sponsorship_op.type = Xdr.const.REVOKE_SPONSORSHIP_SIGNER
            revoke_sponsorship_op.signer = signer
            body.revokeSponsorshipOp = revoke_sponsorship_op
            return body
        else:
            raise ValueError(
                f"{self.revoke_sponsorship_type} is not a valid RevokeSponsorshipType."
            )

    @classmethod
    def from_xdr_object(
        cls, operation_xdr_object: Xdr.types.Operation
    ) -> "RevokeSponsorship":
        """Creates a :class:`RevokeSponsorship` object from an XDR Operation
        object.
        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)
        op_type = operation_xdr_object.body.revokeSponsorshipOp.type
        if op_type == Xdr.const.REVOKE_SPONSORSHIP_LEDGER_ENTRY:
            ledger_key = operation_xdr_object.body.revokeSponsorshipOp.ledgerKey
            ledger_key_type = ledger_key.type
            if ledger_key_type == Xdr.const.ACCOUNT:
                account_id = StrKey.encode_ed25519_public_key(
                    ledger_key.account.accountID.ed25519
                )
                op = cls.revoke_account_sponsorship(account_id, source)
            elif ledger_key_type == Xdr.const.TRUSTLINE:
                account_id = StrKey.encode_ed25519_public_key(
                    ledger_key.trustLine.accountID.ed25519
                )
                asset = Asset.from_xdr_object(ledger_key.trustLine.asset)
                op = cls.revoke_trustline_sponsorship(account_id, asset, source)
            elif ledger_key_type == Xdr.const.OFFER:
                seller_id = StrKey.encode_ed25519_public_key(
                    ledger_key.offer.sellerID.ed25519
                )
                offer_id = ledger_key.offer.offerID
                op = cls.revoke_offer_sponsorship(seller_id, offer_id, source)
            elif ledger_key_type == Xdr.const.DATA:
                account_id = StrKey.encode_ed25519_public_key(
                    ledger_key.data.accountID.ed25519
                )
                data_name = ledger_key.data.dataName.decode()
                op = cls.revoke_data_sponsorship(account_id, data_name, source)
            elif ledger_key_type == Xdr.const.CLAIMABLE_BALANCE:
                balance_id = b"\x00" * 4 + ledger_key.claimableBalance.balanceID.v0
                balance_id = binascii.hexlify(balance_id).decode()
                op = cls.revoke_claimable_balance_sponsorship(balance_id, source)
            else:
                raise ValueError(f"{ledger_key_type} is an unsupported LedgerKey type.")
        elif op_type == Xdr.const.REVOKE_SPONSORSHIP_SIGNER:
            account_id = StrKey.encode_ed25519_public_key(
                operation_xdr_object.body.revokeSponsorshipOp.signer.accountID.ed25519
            )
            signer_key = SignerKey.from_xdr_object(
                operation_xdr_object.body.revokeSponsorshipOp.signer.signerKey
            )
            op = cls.revoke_signer_sponsorship(account_id, signer_key, source)
        else:
            raise ValueError(f"{op_type} is an unsupported RevokeSponsorship type.")
        op._source_muxed = Operation.get_source_muxed_from_xdr_obj(operation_xdr_object)
        return op
