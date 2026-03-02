# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .account_entry import AccountEntry
from .base import DEFAULT_XDR_MAX_DEPTH
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
        account: Optional[AccountEntry] = None,
        trust_line: Optional[TrustLineEntry] = None,
        offer: Optional[OfferEntry] = None,
        data: Optional[DataEntry] = None,
        claimable_balance: Optional[ClaimableBalanceEntry] = None,
        liquidity_pool: Optional[LiquidityPoolEntry] = None,
        contract_data: Optional[ContractDataEntry] = None,
        contract_code: Optional[ContractCodeEntry] = None,
        config_setting: Optional[ConfigSettingEntry] = None,
        ttl: Optional[TTLEntry] = None,
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
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> LedgerEntryData:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = LedgerEntryType.unpack(unpacker)
        if type == LedgerEntryType.ACCOUNT:
            account = AccountEntry.unpack(unpacker, depth_limit - 1)
            return cls(type=type, account=account)
        if type == LedgerEntryType.TRUSTLINE:
            trust_line = TrustLineEntry.unpack(unpacker, depth_limit - 1)
            return cls(type=type, trust_line=trust_line)
        if type == LedgerEntryType.OFFER:
            offer = OfferEntry.unpack(unpacker, depth_limit - 1)
            return cls(type=type, offer=offer)
        if type == LedgerEntryType.DATA:
            data = DataEntry.unpack(unpacker, depth_limit - 1)
            return cls(type=type, data=data)
        if type == LedgerEntryType.CLAIMABLE_BALANCE:
            claimable_balance = ClaimableBalanceEntry.unpack(unpacker, depth_limit - 1)
            return cls(type=type, claimable_balance=claimable_balance)
        if type == LedgerEntryType.LIQUIDITY_POOL:
            liquidity_pool = LiquidityPoolEntry.unpack(unpacker, depth_limit - 1)
            return cls(type=type, liquidity_pool=liquidity_pool)
        if type == LedgerEntryType.CONTRACT_DATA:
            contract_data = ContractDataEntry.unpack(unpacker, depth_limit - 1)
            return cls(type=type, contract_data=contract_data)
        if type == LedgerEntryType.CONTRACT_CODE:
            contract_code = ContractCodeEntry.unpack(unpacker, depth_limit - 1)
            return cls(type=type, contract_code=contract_code)
        if type == LedgerEntryType.CONFIG_SETTING:
            config_setting = ConfigSettingEntry.unpack(unpacker, depth_limit - 1)
            return cls(type=type, config_setting=config_setting)
        if type == LedgerEntryType.TTL:
            ttl = TTLEntry.unpack(unpacker, depth_limit - 1)
            return cls(type=type, ttl=ttl)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerEntryData:
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
    def from_xdr(cls, xdr: str) -> LedgerEntryData:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LedgerEntryData:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.type == LedgerEntryType.ACCOUNT:
            assert self.account is not None
            return {"account": self.account.to_json_dict()}
        if self.type == LedgerEntryType.TRUSTLINE:
            assert self.trust_line is not None
            return {"trustline": self.trust_line.to_json_dict()}
        if self.type == LedgerEntryType.OFFER:
            assert self.offer is not None
            return {"offer": self.offer.to_json_dict()}
        if self.type == LedgerEntryType.DATA:
            assert self.data is not None
            return {"data": self.data.to_json_dict()}
        if self.type == LedgerEntryType.CLAIMABLE_BALANCE:
            assert self.claimable_balance is not None
            return {"claimable_balance": self.claimable_balance.to_json_dict()}
        if self.type == LedgerEntryType.LIQUIDITY_POOL:
            assert self.liquidity_pool is not None
            return {"liquidity_pool": self.liquidity_pool.to_json_dict()}
        if self.type == LedgerEntryType.CONTRACT_DATA:
            assert self.contract_data is not None
            return {"contract_data": self.contract_data.to_json_dict()}
        if self.type == LedgerEntryType.CONTRACT_CODE:
            assert self.contract_code is not None
            return {"contract_code": self.contract_code.to_json_dict()}
        if self.type == LedgerEntryType.CONFIG_SETTING:
            assert self.config_setting is not None
            return {"config_setting": self.config_setting.to_json_dict()}
        if self.type == LedgerEntryType.TTL:
            assert self.ttl is not None
            return {"ttl": self.ttl.to_json_dict()}
        raise ValueError(f"Unknown type in LedgerEntryData: {self.type}")

    @classmethod
    def from_json_dict(cls, json_value: dict) -> LedgerEntryData:
        if len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for LedgerEntryData, got: {json_value}"
            )
        key = next(iter(json_value))
        type = LedgerEntryType.from_json_dict(key)
        if key == "account":
            account = AccountEntry.from_json_dict(json_value["account"])
            return cls(type=type, account=account)
        if key == "trustline":
            trust_line = TrustLineEntry.from_json_dict(json_value["trustline"])
            return cls(type=type, trust_line=trust_line)
        if key == "offer":
            offer = OfferEntry.from_json_dict(json_value["offer"])
            return cls(type=type, offer=offer)
        if key == "data":
            data = DataEntry.from_json_dict(json_value["data"])
            return cls(type=type, data=data)
        if key == "claimable_balance":
            claimable_balance = ClaimableBalanceEntry.from_json_dict(
                json_value["claimable_balance"]
            )
            return cls(type=type, claimable_balance=claimable_balance)
        if key == "liquidity_pool":
            liquidity_pool = LiquidityPoolEntry.from_json_dict(
                json_value["liquidity_pool"]
            )
            return cls(type=type, liquidity_pool=liquidity_pool)
        if key == "contract_data":
            contract_data = ContractDataEntry.from_json_dict(
                json_value["contract_data"]
            )
            return cls(type=type, contract_data=contract_data)
        if key == "contract_code":
            contract_code = ContractCodeEntry.from_json_dict(
                json_value["contract_code"]
            )
            return cls(type=type, contract_code=contract_code)
        if key == "config_setting":
            config_setting = ConfigSettingEntry.from_json_dict(
                json_value["config_setting"]
            )
            return cls(type=type, config_setting=config_setting)
        if key == "ttl":
            ttl = TTLEntry.from_json_dict(json_value["ttl"])
            return cls(type=type, ttl=ttl)
        raise ValueError(f"Unknown key '{key}' for LedgerEntryData")

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
        if self.account is not None:
            out.append(f"account={self.account}")
        if self.trust_line is not None:
            out.append(f"trust_line={self.trust_line}")
        if self.offer is not None:
            out.append(f"offer={self.offer}")
        if self.data is not None:
            out.append(f"data={self.data}")
        if self.claimable_balance is not None:
            out.append(f"claimable_balance={self.claimable_balance}")
        if self.liquidity_pool is not None:
            out.append(f"liquidity_pool={self.liquidity_pool}")
        if self.contract_data is not None:
            out.append(f"contract_data={self.contract_data}")
        if self.contract_code is not None:
            out.append(f"contract_code={self.contract_code}")
        if self.config_setting is not None:
            out.append(f"config_setting={self.config_setting}")
        if self.ttl is not None:
            out.append(f"ttl={self.ttl}")
        return f"<LedgerEntryData [{', '.join(out)}]>"
