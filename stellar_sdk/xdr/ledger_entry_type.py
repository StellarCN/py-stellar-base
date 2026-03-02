# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_LEDGER_ENTRY_TYPE_MAP = {
    0: "account",
    1: "trustline",
    2: "offer",
    3: "data",
    4: "claimable_balance",
    5: "liquidity_pool",
    6: "contract_data",
    7: "contract_code",
    8: "config_setting",
    9: "ttl",
}
_LEDGER_ENTRY_TYPE_REVERSE_MAP = {
    "account": 0,
    "trustline": 1,
    "offer": 2,
    "data": 3,
    "claimable_balance": 4,
    "liquidity_pool": 5,
    "contract_data": 6,
    "contract_code": 7,
    "config_setting": 8,
    "ttl": 9,
}
__all__ = ["LedgerEntryType"]


class LedgerEntryType(IntEnum):
    """
    XDR Source Code::

        enum LedgerEntryType
        {
            ACCOUNT = 0,
            TRUSTLINE = 1,
            OFFER = 2,
            DATA = 3,
            CLAIMABLE_BALANCE = 4,
            LIQUIDITY_POOL = 5,
            CONTRACT_DATA = 6,
            CONTRACT_CODE = 7,
            CONFIG_SETTING = 8,
            TTL = 9
        };
    """

    ACCOUNT = 0
    TRUSTLINE = 1
    OFFER = 2
    DATA = 3
    CLAIMABLE_BALANCE = 4
    LIQUIDITY_POOL = 5
    CONTRACT_DATA = 6
    CONTRACT_CODE = 7
    CONFIG_SETTING = 8
    TTL = 9

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> LedgerEntryType:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerEntryType:
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
    def from_xdr(cls, xdr: str) -> LedgerEntryType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LedgerEntryType:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _LEDGER_ENTRY_TYPE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> LedgerEntryType:
        return cls(_LEDGER_ENTRY_TYPE_REVERSE_MAP[json_value])
