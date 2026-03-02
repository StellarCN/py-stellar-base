# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .config_upgrade_set_key import ConfigUpgradeSetKey
from .ledger_upgrade_type import LedgerUpgradeType
from .uint32 import Uint32

__all__ = ["LedgerUpgrade"]


class LedgerUpgrade:
    """
    XDR Source Code::

        union LedgerUpgrade switch (LedgerUpgradeType type)
        {
        case LEDGER_UPGRADE_VERSION:
            uint32 newLedgerVersion; // update ledgerVersion
        case LEDGER_UPGRADE_BASE_FEE:
            uint32 newBaseFee; // update baseFee
        case LEDGER_UPGRADE_MAX_TX_SET_SIZE:
            uint32 newMaxTxSetSize; // update maxTxSetSize
        case LEDGER_UPGRADE_BASE_RESERVE:
            uint32 newBaseReserve; // update baseReserve
        case LEDGER_UPGRADE_FLAGS:
            uint32 newFlags; // update flags
        case LEDGER_UPGRADE_CONFIG:
            // Update arbitrary `ConfigSetting` entries identified by the key.
            ConfigUpgradeSetKey newConfig;
        case LEDGER_UPGRADE_MAX_SOROBAN_TX_SET_SIZE:
            // Update ConfigSettingContractExecutionLanesV0.ledgerMaxTxCount without
            // using `LEDGER_UPGRADE_CONFIG`.
            uint32 newMaxSorobanTxSetSize;
        };
    """

    def __init__(
        self,
        type: LedgerUpgradeType,
        new_ledger_version: Optional[Uint32] = None,
        new_base_fee: Optional[Uint32] = None,
        new_max_tx_set_size: Optional[Uint32] = None,
        new_base_reserve: Optional[Uint32] = None,
        new_flags: Optional[Uint32] = None,
        new_config: Optional[ConfigUpgradeSetKey] = None,
        new_max_soroban_tx_set_size: Optional[Uint32] = None,
    ) -> None:
        self.type = type
        self.new_ledger_version = new_ledger_version
        self.new_base_fee = new_base_fee
        self.new_max_tx_set_size = new_max_tx_set_size
        self.new_base_reserve = new_base_reserve
        self.new_flags = new_flags
        self.new_config = new_config
        self.new_max_soroban_tx_set_size = new_max_soroban_tx_set_size

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == LedgerUpgradeType.LEDGER_UPGRADE_VERSION:
            if self.new_ledger_version is None:
                raise ValueError("new_ledger_version should not be None.")
            self.new_ledger_version.pack(packer)
            return
        if self.type == LedgerUpgradeType.LEDGER_UPGRADE_BASE_FEE:
            if self.new_base_fee is None:
                raise ValueError("new_base_fee should not be None.")
            self.new_base_fee.pack(packer)
            return
        if self.type == LedgerUpgradeType.LEDGER_UPGRADE_MAX_TX_SET_SIZE:
            if self.new_max_tx_set_size is None:
                raise ValueError("new_max_tx_set_size should not be None.")
            self.new_max_tx_set_size.pack(packer)
            return
        if self.type == LedgerUpgradeType.LEDGER_UPGRADE_BASE_RESERVE:
            if self.new_base_reserve is None:
                raise ValueError("new_base_reserve should not be None.")
            self.new_base_reserve.pack(packer)
            return
        if self.type == LedgerUpgradeType.LEDGER_UPGRADE_FLAGS:
            if self.new_flags is None:
                raise ValueError("new_flags should not be None.")
            self.new_flags.pack(packer)
            return
        if self.type == LedgerUpgradeType.LEDGER_UPGRADE_CONFIG:
            if self.new_config is None:
                raise ValueError("new_config should not be None.")
            self.new_config.pack(packer)
            return
        if self.type == LedgerUpgradeType.LEDGER_UPGRADE_MAX_SOROBAN_TX_SET_SIZE:
            if self.new_max_soroban_tx_set_size is None:
                raise ValueError("new_max_soroban_tx_set_size should not be None.")
            self.new_max_soroban_tx_set_size.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> LedgerUpgrade:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = LedgerUpgradeType.unpack(unpacker)
        if type == LedgerUpgradeType.LEDGER_UPGRADE_VERSION:
            new_ledger_version = Uint32.unpack(unpacker, depth_limit - 1)
            return cls(type=type, new_ledger_version=new_ledger_version)
        if type == LedgerUpgradeType.LEDGER_UPGRADE_BASE_FEE:
            new_base_fee = Uint32.unpack(unpacker, depth_limit - 1)
            return cls(type=type, new_base_fee=new_base_fee)
        if type == LedgerUpgradeType.LEDGER_UPGRADE_MAX_TX_SET_SIZE:
            new_max_tx_set_size = Uint32.unpack(unpacker, depth_limit - 1)
            return cls(type=type, new_max_tx_set_size=new_max_tx_set_size)
        if type == LedgerUpgradeType.LEDGER_UPGRADE_BASE_RESERVE:
            new_base_reserve = Uint32.unpack(unpacker, depth_limit - 1)
            return cls(type=type, new_base_reserve=new_base_reserve)
        if type == LedgerUpgradeType.LEDGER_UPGRADE_FLAGS:
            new_flags = Uint32.unpack(unpacker, depth_limit - 1)
            return cls(type=type, new_flags=new_flags)
        if type == LedgerUpgradeType.LEDGER_UPGRADE_CONFIG:
            new_config = ConfigUpgradeSetKey.unpack(unpacker, depth_limit - 1)
            return cls(type=type, new_config=new_config)
        if type == LedgerUpgradeType.LEDGER_UPGRADE_MAX_SOROBAN_TX_SET_SIZE:
            new_max_soroban_tx_set_size = Uint32.unpack(unpacker, depth_limit - 1)
            return cls(
                type=type, new_max_soroban_tx_set_size=new_max_soroban_tx_set_size
            )
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerUpgrade:
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
    def from_xdr(cls, xdr: str) -> LedgerUpgrade:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LedgerUpgrade:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.type == LedgerUpgradeType.LEDGER_UPGRADE_VERSION:
            assert self.new_ledger_version is not None
            return {"version": self.new_ledger_version.to_json_dict()}
        if self.type == LedgerUpgradeType.LEDGER_UPGRADE_BASE_FEE:
            assert self.new_base_fee is not None
            return {"base_fee": self.new_base_fee.to_json_dict()}
        if self.type == LedgerUpgradeType.LEDGER_UPGRADE_MAX_TX_SET_SIZE:
            assert self.new_max_tx_set_size is not None
            return {"max_tx_set_size": self.new_max_tx_set_size.to_json_dict()}
        if self.type == LedgerUpgradeType.LEDGER_UPGRADE_BASE_RESERVE:
            assert self.new_base_reserve is not None
            return {"base_reserve": self.new_base_reserve.to_json_dict()}
        if self.type == LedgerUpgradeType.LEDGER_UPGRADE_FLAGS:
            assert self.new_flags is not None
            return {"flags": self.new_flags.to_json_dict()}
        if self.type == LedgerUpgradeType.LEDGER_UPGRADE_CONFIG:
            assert self.new_config is not None
            return {"config": self.new_config.to_json_dict()}
        if self.type == LedgerUpgradeType.LEDGER_UPGRADE_MAX_SOROBAN_TX_SET_SIZE:
            assert self.new_max_soroban_tx_set_size is not None
            return {
                "max_soroban_tx_set_size": self.new_max_soroban_tx_set_size.to_json_dict()
            }
        raise ValueError(f"Unknown type in LedgerUpgrade: {self.type}")

    @classmethod
    def from_json_dict(cls, json_value: dict) -> LedgerUpgrade:
        if len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for LedgerUpgrade, got: {json_value}"
            )
        key = next(iter(json_value))
        type = LedgerUpgradeType.from_json_dict(key)
        if key == "version":
            new_ledger_version = Uint32.from_json_dict(json_value["version"])
            return cls(type=type, new_ledger_version=new_ledger_version)
        if key == "base_fee":
            new_base_fee = Uint32.from_json_dict(json_value["base_fee"])
            return cls(type=type, new_base_fee=new_base_fee)
        if key == "max_tx_set_size":
            new_max_tx_set_size = Uint32.from_json_dict(json_value["max_tx_set_size"])
            return cls(type=type, new_max_tx_set_size=new_max_tx_set_size)
        if key == "base_reserve":
            new_base_reserve = Uint32.from_json_dict(json_value["base_reserve"])
            return cls(type=type, new_base_reserve=new_base_reserve)
        if key == "flags":
            new_flags = Uint32.from_json_dict(json_value["flags"])
            return cls(type=type, new_flags=new_flags)
        if key == "config":
            new_config = ConfigUpgradeSetKey.from_json_dict(json_value["config"])
            return cls(type=type, new_config=new_config)
        if key == "max_soroban_tx_set_size":
            new_max_soroban_tx_set_size = Uint32.from_json_dict(
                json_value["max_soroban_tx_set_size"]
            )
            return cls(
                type=type, new_max_soroban_tx_set_size=new_max_soroban_tx_set_size
            )
        raise ValueError(f"Unknown key '{key}' for LedgerUpgrade")

    def __hash__(self):
        return hash(
            (
                self.type,
                self.new_ledger_version,
                self.new_base_fee,
                self.new_max_tx_set_size,
                self.new_base_reserve,
                self.new_flags,
                self.new_config,
                self.new_max_soroban_tx_set_size,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.new_ledger_version == other.new_ledger_version
            and self.new_base_fee == other.new_base_fee
            and self.new_max_tx_set_size == other.new_max_tx_set_size
            and self.new_base_reserve == other.new_base_reserve
            and self.new_flags == other.new_flags
            and self.new_config == other.new_config
            and self.new_max_soroban_tx_set_size == other.new_max_soroban_tx_set_size
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        if self.new_ledger_version is not None:
            out.append(f"new_ledger_version={self.new_ledger_version}")
        if self.new_base_fee is not None:
            out.append(f"new_base_fee={self.new_base_fee}")
        if self.new_max_tx_set_size is not None:
            out.append(f"new_max_tx_set_size={self.new_max_tx_set_size}")
        if self.new_base_reserve is not None:
            out.append(f"new_base_reserve={self.new_base_reserve}")
        if self.new_flags is not None:
            out.append(f"new_flags={self.new_flags}")
        if self.new_config is not None:
            out.append(f"new_config={self.new_config}")
        if self.new_max_soroban_tx_set_size is not None:
            out.append(
                f"new_max_soroban_tx_set_size={self.new_max_soroban_tx_set_size}"
            )
        return f"<LedgerUpgrade [{', '.join(out)}]>"
