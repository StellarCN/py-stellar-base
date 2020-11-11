import base64
import binascii
from enum import IntEnum
from typing import Optional

from .operation import Operation
from .operation_type import OperationType
from .utils import check_ed25519_public_key
from .. import xdr as stellar_xdr
from ..asset import Asset
from ..exceptions import ValueError
from ..keypair import Keypair
from ..signer_key import SignerKey
from ..strkey import StrKey


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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.account_id == other.account_id and self.asset == other.asset

    def __str__(self):
        return f"<TrustLine [account_id={self.account_id}, asset={self.asset}]>"


class Offer:
    def __init__(self, seller_id: str, offer_id: int) -> None:
        check_ed25519_public_key(seller_id)
        self.seller_id = seller_id
        self.offer_id = offer_id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.seller_id == other.seller_id and self.offer_id == other.offer_id

    def __str__(self):
        return f"<Offer [seller_id={self.seller_id}, offer_id={self.offer_id}]>"


class Data:
    def __init__(self, account_id: str, data_name: str) -> None:
        check_ed25519_public_key(account_id)
        self.account_id = account_id
        self.data_name = data_name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.account_id == other.account_id and self.data_name == other.data_name

    def __str__(self):
        return f"<Data [account_id={self.account_id}, data_name={self.data_name}]>"


class Signer:
    def __init__(self, account_id: str, signer_key: SignerKey) -> None:
        check_ed25519_public_key(account_id)
        self.account_id = account_id
        self.signer_key = signer_key

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return (
            self.account_id == other.account_id and self.signer_key == other.signer_key
        )

    def __str__(self):
        return f"<Signer [account_id={self.account_id}, signer_key={self.signer_key}]>"


class RevokeSponsorship(Operation):
    """The :class:`RevokeSponsorship` object, which represents a RevokeSponsorship
    operation on Stellar's network.

    The logic of this operation depends on the state of the source account.

    If the source account is not sponsored or is sponsored by the owner of the specified entry or sub-entry,
    then attempt to revoke the sponsorship. If the source account is sponsored, the next step depends on whether the
    entry is sponsored or not. If it is sponsored, attempt to transfer the sponsorship to the sponsor
    of the source account. If the entry is not sponsored, then establish the sponsorship.
    See `Sponsored Reserves <https://developers.stellar.org/docs/glossary/sponsored-reserves/>_` for more information.

    See `Revoke Sponsorship
    <https://developers.stellar.org/docs/start/list-of-operations/#revoke-sponsorship>_`.

    Threshold: Medium

    :param revoke_sponsorship_type: The sponsored account id.
    :param account_id: The sponsored account ID.
    :param trustline: The sponsored trustline.
    :param offer: The sponsored offer.
    :param data: The sponsored data.
    :param claimable_balance_id: The sponsored claimable balance.
    :param signer: The sponsored signer.
    :param source: The source account (defaults to transaction source).
    """
    _TYPE: stellar_xdr.OperationType = stellar_xdr.OperationType.REVOKE_SPONSORSHIP
    TYPE: OperationType = OperationType.REVOKE_SPONSORSHIP

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

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        if self.revoke_sponsorship_type == RevokeSponsorshipType.ACCOUNT:
            assert self.account_id is not None
            account = stellar_xdr.LedgerKeyAccount(
                Keypair.from_public_key(self.account_id).xdr_account_id()
            )
            ledger_key = stellar_xdr.LedgerKey(
                stellar_xdr.LedgerEntryType.ACCOUNT, account=account
            )
            revoke_sponsorship_op = stellar_xdr.RevokeSponsorshipOp(
                stellar_xdr.RevokeSponsorshipType.REVOKE_SPONSORSHIP_LEDGER_ENTRY,
                ledger_key=ledger_key,
            )
        elif self.revoke_sponsorship_type == RevokeSponsorshipType.TRUSTLINE:
            assert self.trustline is not None
            trust_line = stellar_xdr.LedgerKeyTrustLine(
                Keypair.from_public_key(self.trustline.account_id).xdr_account_id(),
                self.trustline.asset.to_xdr_object(),
            )
            ledger_key = stellar_xdr.LedgerKey(
                stellar_xdr.LedgerEntryType.TRUSTLINE, trust_line=trust_line
            )
            revoke_sponsorship_op = stellar_xdr.RevokeSponsorshipOp(
                stellar_xdr.RevokeSponsorshipType.REVOKE_SPONSORSHIP_LEDGER_ENTRY,
                ledger_key=ledger_key,
            )
        elif self.revoke_sponsorship_type == RevokeSponsorshipType.OFFER:
            assert self.offer is not None
            offer = stellar_xdr.LedgerKeyOffer(
                Keypair.from_public_key(self.offer.seller_id).xdr_account_id(),
                stellar_xdr.Int64(self.offer.offer_id),
            )
            ledger_key = stellar_xdr.LedgerKey(
                stellar_xdr.LedgerEntryType.OFFER, offer=offer
            )
            revoke_sponsorship_op = stellar_xdr.RevokeSponsorshipOp(
                stellar_xdr.RevokeSponsorshipType.REVOKE_SPONSORSHIP_LEDGER_ENTRY,
                ledger_key=ledger_key,
            )
        elif self.revoke_sponsorship_type == RevokeSponsorshipType.DATA:
            assert self.data is not None
            data = stellar_xdr.LedgerKeyData(
                Keypair.from_public_key(self.data.account_id).xdr_account_id(),
                stellar_xdr.String64(self.data.data_name.encode()),
            )
            ledger_key = stellar_xdr.LedgerKey(
                stellar_xdr.LedgerEntryType.DATA, data=data
            )
            revoke_sponsorship_op = stellar_xdr.RevokeSponsorshipOp(
                stellar_xdr.RevokeSponsorshipType.REVOKE_SPONSORSHIP_LEDGER_ENTRY,
                ledger_key=ledger_key,
            )
        elif self.revoke_sponsorship_type == RevokeSponsorshipType.CLAIMABLE_BALANCE:
            assert self.claimable_balance_id is not None
            claimable_balance_bytes = binascii.unhexlify(self.claimable_balance_id)
            balance_id = stellar_xdr.ClaimableBalanceID.from_xdr_bytes(
                claimable_balance_bytes
            )
            claimable_balance = stellar_xdr.LedgerKeyClaimableBalance(
                balance_id=balance_id
            )
            ledger_key = stellar_xdr.LedgerKey(
                stellar_xdr.LedgerEntryType.CLAIMABLE_BALANCE,
                claimable_balance=claimable_balance,
            )
            revoke_sponsorship_op = stellar_xdr.RevokeSponsorshipOp(
                stellar_xdr.RevokeSponsorshipType.REVOKE_SPONSORSHIP_LEDGER_ENTRY,
                ledger_key=ledger_key,
            )
        elif self.revoke_sponsorship_type == RevokeSponsorshipType.SIGNER:
            assert self.signer is not None
            signer_key = stellar_xdr.RevokeSponsorshipOpSigner(
                Keypair.from_public_key(self.signer.account_id).xdr_account_id(),
                self.signer.signer_key.to_xdr_object(),
            )
            revoke_sponsorship_op = stellar_xdr.RevokeSponsorshipOp(
                stellar_xdr.RevokeSponsorshipType.REVOKE_SPONSORSHIP_SIGNER,
                signer=signer_key,
            )
        else:
            raise ValueError(
                f"{self.revoke_sponsorship_type} is not a valid RevokeSponsorshipType."
            )
        body = stellar_xdr.OperationBody(
            type=self._TYPE, revoke_sponsorship_op=revoke_sponsorship_op
        )
        return body

    @classmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.Operation
    ) -> "RevokeSponsorship":
        """Creates a :class:`RevokeSponsorship` object from an XDR Operation
        object.
        """
        source = Operation.get_source_from_xdr_obj(xdr_object)
        assert xdr_object.body.revoke_sponsorship_op is not None
        op_type = xdr_object.body.revoke_sponsorship_op.type
        if op_type == stellar_xdr.RevokeSponsorshipType.REVOKE_SPONSORSHIP_LEDGER_ENTRY:
            assert xdr_object.body.revoke_sponsorship_op is not None
            ledger_key = xdr_object.body.revoke_sponsorship_op.ledger_key
            assert ledger_key is not None
            assert ledger_key.type is not None
            ledger_key_type = ledger_key.type
            if ledger_key_type == stellar_xdr.LedgerEntryType.ACCOUNT:
                assert ledger_key.account is not None
                assert ledger_key.account.account_id.account_id.ed25519 is not None
                account_id = StrKey.encode_ed25519_public_key(
                    ledger_key.account.account_id.account_id.ed25519.uint256
                )
                op = cls.revoke_account_sponsorship(account_id, source)
            elif ledger_key_type == stellar_xdr.LedgerEntryType.TRUSTLINE:
                assert ledger_key.trust_line is not None
                assert ledger_key.trust_line.account_id is not None
                assert ledger_key.trust_line.account_id.account_id.ed25519 is not None
                account_id = StrKey.encode_ed25519_public_key(
                    ledger_key.trust_line.account_id.account_id.ed25519.uint256
                )
                asset = Asset.from_xdr_object(ledger_key.trust_line.asset)
                op = cls.revoke_trustline_sponsorship(account_id, asset, source)
            elif ledger_key_type == stellar_xdr.LedgerEntryType.OFFER:
                assert ledger_key.offer is not None
                assert ledger_key.offer.seller_id.account_id.ed25519 is not None
                seller_id = StrKey.encode_ed25519_public_key(
                    ledger_key.offer.seller_id.account_id.ed25519.uint256
                )
                offer_id = ledger_key.offer.offer_id.int64
                op = cls.revoke_offer_sponsorship(seller_id, offer_id, source)
            elif ledger_key_type == stellar_xdr.LedgerEntryType.DATA:
                assert ledger_key.data is not None
                assert ledger_key.data.account_id is not None
                assert ledger_key.data.account_id.account_id is not None
                assert ledger_key.data.account_id.account_id.ed25519 is not None
                account_id = StrKey.encode_ed25519_public_key(
                    ledger_key.data.account_id.account_id.ed25519.uint256
                )
                data_name = ledger_key.data.data_name.string64.decode()
                op = cls.revoke_data_sponsorship(account_id, data_name, source)
            elif ledger_key_type == stellar_xdr.LedgerEntryType.CLAIMABLE_BALANCE:
                assert ledger_key.claimable_balance is not None
                balance_id_bytes = base64.b64decode(
                    ledger_key.claimable_balance.balance_id.to_xdr()
                )
                balance_id = binascii.hexlify(balance_id_bytes).decode()
                op = cls.revoke_claimable_balance_sponsorship(balance_id, source)
            else:
                raise ValueError(f"{ledger_key_type} is an unsupported LedgerKey type.")
        elif op_type == stellar_xdr.RevokeSponsorshipType.REVOKE_SPONSORSHIP_SIGNER:
            assert xdr_object.body.revoke_sponsorship_op.signer is not None
            assert xdr_object.body.revoke_sponsorship_op.signer.account_id.account_id.ed25519 is not None
            account_id = StrKey.encode_ed25519_public_key(
                xdr_object.body.revoke_sponsorship_op.signer.account_id.account_id.ed25519.uint256
            )
            signer_key = SignerKey.from_xdr_object(
                xdr_object.body.revoke_sponsorship_op.signer.signer_key
            )
            op = cls.revoke_signer_sponsorship(account_id, signer_key, source)
        else:
            raise ValueError(f"{op_type} is an unsupported RevokeSponsorship type.")
        op._source_muxed = Operation.get_source_muxed_from_xdr_obj(xdr_object)
        return op

    def __str__(self):
        return (
            f"<RevokeSponsorship [revoke_sponsorship_type={self.revoke_sponsorship_type}, "
            f"account_id={self.account_id}, "
            f"trustline={self.trustline}, "
            f"offer={self.offer}, "
            f"data={self.data}, "
            f"claimable_balance_id={self.claimable_balance_id}, "
            f"signer={self.signer}, "
            f"source={self.source}]>"
        )
