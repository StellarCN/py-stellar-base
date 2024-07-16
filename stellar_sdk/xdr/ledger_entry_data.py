# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .account_entry import AccountEntry
from .claimable_balance_entry import ClaimableBalanceEntry
from .config_setting_entry import ConfigSettingEntry
from .contract_code_entry import ContractCodeEntry
from .contract_data_entry import ContractDataEntry
from .data_entry import DataEntry
from .ledger_entry_type import LedgerEntryType
from .liquidity_pool_entry import LiquidityPoolEntry
from .offer_entry import OfferEntry
from .trust_line_entry import TrustLineEntry
from .ttl_entry import TTLEntry

__all__ = ["LedgerEntryData"]


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
            case CONTRACT_DATA:
                ContractDataEntry contractData;
            case CONTRACT_CODE:
                ContractCodeEntry contractCode;
            case CONFIG_SETTING:
                ConfigSettingEntry configSetting;
            case TTL:
                TTLEntry ttl;
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
        contract_data: ContractDataEntry = None,
        contract_code: ContractCodeEntry = None,
        config_setting: ConfigSettingEntry = None,
        ttl: TTLEntry = None,
    ) -> None:
        self.type = type
        self.account = account
        self.trust_line = trust_line
        self.offer = offer
        self.data = data
        self.claimable_balance = claimable_balance
        self.liquidity_pool = liquidity_pool
        self.contract_data = contract_data
        self.contract_code = contract_code
        self.config_setting = config_setting
        self.ttl = ttl

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
        if self.type == LedgerEntryType.CONTRACT_DATA:
            if self.contract_data is None:
                raise ValueError("contract_data should not be None.")
            self.contract_data.pack(packer)
            return
        if self.type == LedgerEntryType.CONTRACT_CODE:
            if self.contract_code is None:
                raise ValueError("contract_code should not be None.")
            self.contract_code.pack(packer)
            return
        if self.type == LedgerEntryType.CONFIG_SETTING:
            if self.config_setting is None:
                raise ValueError("config_setting should not be None.")
            self.config_setting.pack(packer)
            return
        if self.type == LedgerEntryType.TTL:
            if self.ttl is None:
                raise ValueError("ttl should not be None.")
            self.ttl.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> LedgerEntryData:
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
        if type == LedgerEntryType.CONTRACT_DATA:
            contract_data = ContractDataEntry.unpack(unpacker)
            return cls(type=type, contract_data=contract_data)
        if type == LedgerEntryType.CONTRACT_CODE:
            contract_code = ContractCodeEntry.unpack(unpacker)
            return cls(type=type, contract_code=contract_code)
        if type == LedgerEntryType.CONFIG_SETTING:
            config_setting = ConfigSettingEntry.unpack(unpacker)
            return cls(type=type, config_setting=config_setting)
        if type == LedgerEntryType.TTL:
            ttl = TTLEntry.unpack(unpacker)
            return cls(type=type, ttl=ttl)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerEntryData:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LedgerEntryData:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.type,
                self.account,
                self.trust_line,
                self.offer,
                self.data,
                self.claimable_balance,
                self.liquidity_pool,
                self.contract_data,
                self.contract_code,
                self.config_setting,
                self.ttl,
            )
        )

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
            and self.contract_data == other.contract_data
            and self.contract_code == other.contract_code
            and self.config_setting == other.config_setting
            and self.ttl == other.ttl
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"account={self.account}") if self.account is not None else None
        (
            out.append(f"trust_line={self.trust_line}")
            if self.trust_line is not None
            else None
        )
        out.append(f"offer={self.offer}") if self.offer is not None else None
        out.append(f"data={self.data}") if self.data is not None else None
        (
            out.append(f"claimable_balance={self.claimable_balance}")
            if self.claimable_balance is not None
            else None
        )
        (
            out.append(f"liquidity_pool={self.liquidity_pool}")
            if self.liquidity_pool is not None
            else None
        )
        (
            out.append(f"contract_data={self.contract_data}")
            if self.contract_data is not None
            else None
        )
        (
            out.append(f"contract_code={self.contract_code}")
            if self.contract_code is not None
            else None
        )
        (
            out.append(f"config_setting={self.config_setting}")
            if self.config_setting is not None
            else None
        )
        out.append(f"ttl={self.ttl}") if self.ttl is not None else None
        return f"<LedgerEntryData [{', '.join(out)}]>"
