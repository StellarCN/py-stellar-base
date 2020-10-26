# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .ledger_entry_type import LedgerEntryType
from .ledger_key_account import LedgerKeyAccount
from .ledger_key_claimable_balance import LedgerKeyClaimableBalance
from .ledger_key_data import LedgerKeyData
from .ledger_key_offer import LedgerKeyOffer
from .ledger_key_trust_line import LedgerKeyTrustLine
from ..exceptions import ValueError

__all__ = ["LedgerKey"]


class LedgerKey:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union LedgerKey switch (LedgerEntryType type)
    {
    case ACCOUNT:
        struct
        {
            AccountID accountID;
        } account;
    
    case TRUSTLINE:
        struct
        {
            AccountID accountID;
            Asset asset;
        } trustLine;
    
    case OFFER:
        struct
        {
            AccountID sellerID;
            int64 offerID;
        } offer;
    
    case DATA:
        struct
        {
            AccountID accountID;
            string64 dataName;
        } data;
    
    case CLAIMABLE_BALANCE:
        struct
        {
            ClaimableBalanceID balanceID;
        } claimableBalance;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: LedgerEntryType,
        account: LedgerKeyAccount = None,
        trust_line: LedgerKeyTrustLine = None,
        offer: LedgerKeyOffer = None,
        data: LedgerKeyData = None,
        claimable_balance: LedgerKeyClaimableBalance = None,
    ) -> None:
        self.type = type
        self.account = account
        self.trust_line = trust_line
        self.offer = offer
        self.data = data
        self.claimable_balance = claimable_balance

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == LedgerEntryType.ACCOUNT:
            if self.account is None:
                raise ValueError("account should not be None.")
            self.account.pack(packer)
            return
        if self.type == LedgerEntryType.TRUSTLINE:
            if self.trust_line is None:
                raise ValueError("trust_line should not be None.")
            self.trust_line.pack(packer)
            return
        if self.type == LedgerEntryType.OFFER:
            if self.offer is None:
                raise ValueError("offer should not be None.")
            self.offer.pack(packer)
            return
        if self.type == LedgerEntryType.DATA:
            if self.data is None:
                raise ValueError("data should not be None.")
            self.data.pack(packer)
            return
        if self.type == LedgerEntryType.CLAIMABLE_BALANCE:
            if self.claimable_balance is None:
                raise ValueError("claimable_balance should not be None.")
            self.claimable_balance.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerKey":
        type = LedgerEntryType.unpack(unpacker)
        if type == LedgerEntryType.ACCOUNT:
            account = LedgerKeyAccount.unpack(unpacker)
            if account is None:
                raise ValueError("account should not be None.")
            return cls(type, account=account)
        if type == LedgerEntryType.TRUSTLINE:
            trust_line = LedgerKeyTrustLine.unpack(unpacker)
            if trust_line is None:
                raise ValueError("trust_line should not be None.")
            return cls(type, trust_line=trust_line)
        if type == LedgerEntryType.OFFER:
            offer = LedgerKeyOffer.unpack(unpacker)
            if offer is None:
                raise ValueError("offer should not be None.")
            return cls(type, offer=offer)
        if type == LedgerEntryType.DATA:
            data = LedgerKeyData.unpack(unpacker)
            if data is None:
                raise ValueError("data should not be None.")
            return cls(type, data=data)
        if type == LedgerEntryType.CLAIMABLE_BALANCE:
            claimable_balance = LedgerKeyClaimableBalance.unpack(unpacker)
            if claimable_balance is None:
                raise ValueError("claimable_balance should not be None.")
            return cls(type, claimable_balance=claimable_balance)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "LedgerKey":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerKey":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.account == other.account
            and self.trust_line == other.trust_line
            and self.offer == other.offer
            and self.data == other.data
            and self.claimable_balance == other.claimable_balance
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"account={self.account}") if self.account is not None else None
        out.append(
            f"trust_line={self.trust_line}"
        ) if self.trust_line is not None else None
        out.append(f"offer={self.offer}") if self.offer is not None else None
        out.append(f"data={self.data}") if self.data is not None else None
        out.append(
            f"claimable_balance={self.claimable_balance}"
        ) if self.claimable_balance is not None else None
        return f"<LedgerKey {[', '.join(out)]}>"
