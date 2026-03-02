# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_LEDGER_UPGRADE_TYPE_MAP = {
    1: "version",
    2: "base_fee",
    3: "max_tx_set_size",
    4: "base_reserve",
    5: "flags",
    6: "config",
    7: "max_soroban_tx_set_size",
}
_LEDGER_UPGRADE_TYPE_REVERSE_MAP = {
    "version": 1,
    "base_fee": 2,
    "max_tx_set_size": 3,
    "base_reserve": 4,
    "flags": 5,
    "config": 6,
    "max_soroban_tx_set_size": 7,
}
__all__ = ["LedgerUpgradeType"]


class LedgerUpgradeType(IntEnum):
    """
    XDR Source Code::

        enum LedgerUpgradeType
        {
            LEDGER_UPGRADE_VERSION = 1,
            LEDGER_UPGRADE_BASE_FEE = 2,
            LEDGER_UPGRADE_MAX_TX_SET_SIZE = 3,
            LEDGER_UPGRADE_BASE_RESERVE = 4,
            LEDGER_UPGRADE_FLAGS = 5,
            LEDGER_UPGRADE_CONFIG = 6,
            LEDGER_UPGRADE_MAX_SOROBAN_TX_SET_SIZE = 7
        };
    """

    LEDGER_UPGRADE_VERSION = 1
    LEDGER_UPGRADE_BASE_FEE = 2
    LEDGER_UPGRADE_MAX_TX_SET_SIZE = 3
    LEDGER_UPGRADE_BASE_RESERVE = 4
    LEDGER_UPGRADE_FLAGS = 5
    LEDGER_UPGRADE_CONFIG = 6
    LEDGER_UPGRADE_MAX_SOROBAN_TX_SET_SIZE = 7

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> LedgerUpgradeType:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerUpgradeType:
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
    def from_xdr(cls, xdr: str) -> LedgerUpgradeType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LedgerUpgradeType:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _LEDGER_UPGRADE_TYPE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> LedgerUpgradeType:
        return cls(_LEDGER_UPGRADE_TYPE_REVERSE_MAP[json_value])
