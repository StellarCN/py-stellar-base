# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from ..type_checked import type_checked
from .account_entry import AccountEntry
from .claimable_balance_entry import ClaimableBalanceEntry
from .data_entry import DataEntry
from .ledger_entry_type import LedgerEntryType
from .liquidity_pool_entry import LiquidityPoolEntry
from .offer_entry import OfferEntry
from .trust_line_entry import TrustLineEntry

__all__ = ["LedgerEntryData"]


@type_checked
class LedgerEntryData:
    """
    XDR Source Code::

        union switch (LedgerEntryType type)
            {
            case ACCOUNT:
                AccountEntry account;
            case TRUSTLINE:
                TrustLineEntry trustLine;
            case OFFER:
                OfferEntry offer;
            case DATA:
                DataEntry data;
            case CLAIMABLE_BALANCE:
                ClaimableBalanceEntry claimableBalance;
            case LIQUIDITY_POOL:
                LiquidityPoolEntry liquidityPool;
            }
    """

    def __init__(
        self,
        type: LedgerEntryType,
        account: AccountEntry = None,
        trust_line: TrustLineEntry = None,
        offer: OfferEntry = None,
        data: DataEntry = None,
        claimable_balance: ClaimableBalanceEntry = None,
        liquidity_pool: LiquidityPoolEntry = None,
    ) -> None:
        self.type = type
        self.account = account
        self.trust_line = trust_line
        self.offer = offer
        self.data = data
        self.claimable_balance = claimable_balance
        self.liquidity_pool = liquidity_pool

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
        if self.type == LedgerEntryType.LIQUIDITY_POOL:
            if self.liquidity_pool is None:
                raise ValueError("liquidity_pool should not be None.")
            self.liquidity_pool.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerEntryData":
        type = LedgerEntryType.unpack(unpacker)
        if type == LedgerEntryType.ACCOUNT:
            account = AccountEntry.unpack(unpacker)
            return cls(type=type, account=account)
        if type == LedgerEntryType.TRUSTLINE:
            trust_line = TrustLineEntry.unpack(unpacker)
            return cls(type=type, trust_line=trust_line)
        if type == LedgerEntryType.OFFER:
            offer = OfferEntry.unpack(unpacker)
            return cls(type=type, offer=offer)
        if type == LedgerEntryType.DATA:
            data = DataEntry.unpack(unpacker)
            return cls(type=type, data=data)
        if type == LedgerEntryType.CLAIMABLE_BALANCE:
            claimable_balance = ClaimableBalanceEntry.unpack(unpacker)
            return cls(type=type, claimable_balance=claimable_balance)
        if type == LedgerEntryType.LIQUIDITY_POOL:
            liquidity_pool = LiquidityPoolEntry.unpack(unpacker)
            return cls(type=type, liquidity_pool=liquidity_pool)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "LedgerEntryData":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerEntryData":
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
            and self.liquidity_pool == other.liquidity_pool
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
        out.append(
            f"liquidity_pool={self.liquidity_pool}"
        ) if self.liquidity_pool is not None else None
        return f"<LedgerEntryData {[', '.join(out)]}>"
