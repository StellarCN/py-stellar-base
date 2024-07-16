# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .ledger_entry_type import LedgerEntryType
from .ledger_key_account import LedgerKeyAccount
from .ledger_key_claimable_balance import LedgerKeyClaimableBalance
from .ledger_key_config_setting import LedgerKeyConfigSetting
from .ledger_key_contract_code import LedgerKeyContractCode
from .ledger_key_contract_data import LedgerKeyContractData
from .ledger_key_data import LedgerKeyData
from .ledger_key_liquidity_pool import LedgerKeyLiquidityPool
from .ledger_key_offer import LedgerKeyOffer
from .ledger_key_trust_line import LedgerKeyTrustLine
from .ledger_key_ttl import LedgerKeyTtl

__all__ = ["LedgerKey"]


class LedgerKey:
    """
    XDR Source Code::

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
                TrustLineAsset asset;
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

        case LIQUIDITY_POOL:
            struct
            {
                PoolID liquidityPoolID;
            } liquidityPool;
        case CONTRACT_DATA:
            struct
            {
                SCAddress contract;
                SCVal key;
                ContractDataDurability durability;
            } contractData;
        case CONTRACT_CODE:
            struct
            {
                Hash hash;
            } contractCode;
        case CONFIG_SETTING:
            struct
            {
                ConfigSettingID configSettingID;
            } configSetting;
        case TTL:
            struct
            {
                // Hash of the LedgerKey that is associated with this TTLEntry
                Hash keyHash;
            } ttl;
        };
    """

    def __init__(
        self,
        type: LedgerEntryType,
        account: LedgerKeyAccount = None,
        trust_line: LedgerKeyTrustLine = None,
        offer: LedgerKeyOffer = None,
        data: LedgerKeyData = None,
        claimable_balance: LedgerKeyClaimableBalance = None,
        liquidity_pool: LedgerKeyLiquidityPool = None,
        contract_data: LedgerKeyContractData = None,
        contract_code: LedgerKeyContractCode = None,
        config_setting: LedgerKeyConfigSetting = None,
        ttl: LedgerKeyTtl = None,
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
    def unpack(cls, unpacker: Unpacker) -> LedgerKey:
        type = LedgerEntryType.unpack(unpacker)
        if type == LedgerEntryType.ACCOUNT:
            account = LedgerKeyAccount.unpack(unpacker)
            return cls(type=type, account=account)
        if type == LedgerEntryType.TRUSTLINE:
            trust_line = LedgerKeyTrustLine.unpack(unpacker)
            return cls(type=type, trust_line=trust_line)
        if type == LedgerEntryType.OFFER:
            offer = LedgerKeyOffer.unpack(unpacker)
            return cls(type=type, offer=offer)
        if type == LedgerEntryType.DATA:
            data = LedgerKeyData.unpack(unpacker)
            return cls(type=type, data=data)
        if type == LedgerEntryType.CLAIMABLE_BALANCE:
            claimable_balance = LedgerKeyClaimableBalance.unpack(unpacker)
            return cls(type=type, claimable_balance=claimable_balance)
        if type == LedgerEntryType.LIQUIDITY_POOL:
            liquidity_pool = LedgerKeyLiquidityPool.unpack(unpacker)
            return cls(type=type, liquidity_pool=liquidity_pool)
        if type == LedgerEntryType.CONTRACT_DATA:
            contract_data = LedgerKeyContractData.unpack(unpacker)
            return cls(type=type, contract_data=contract_data)
        if type == LedgerEntryType.CONTRACT_CODE:
            contract_code = LedgerKeyContractCode.unpack(unpacker)
            return cls(type=type, contract_code=contract_code)
        if type == LedgerEntryType.CONFIG_SETTING:
            config_setting = LedgerKeyConfigSetting.unpack(unpacker)
            return cls(type=type, config_setting=config_setting)
        if type == LedgerEntryType.TTL:
            ttl = LedgerKeyTtl.unpack(unpacker)
            return cls(type=type, ttl=ttl)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerKey:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LedgerKey:
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
        return f"<LedgerKey [{', '.join(out)}]>"
