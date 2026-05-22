# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_LEDGER_HEADER_FLAGS_MAP = {1: "trading_flag", 2: "deposit_flag", 4: "withdrawal_flag"}
_LEDGER_HEADER_FLAGS_REVERSE_MAP = {
    "trading_flag": 1,
    "deposit_flag": 2,
    "withdrawal_flag": 4,
}
__all__ = ["LedgerHeaderFlags"]


class LedgerHeaderFlags(IntEnum):
    """
    XDR Source Code::

        enum LedgerHeaderFlags
        {
            DISABLE_LIQUIDITY_POOL_TRADING_FLAG = 0x1,
            DISABLE_LIQUIDITY_POOL_DEPOSIT_FLAG = 0x2,
            DISABLE_LIQUIDITY_POOL_WITHDRAWAL_FLAG = 0x4
        };
    """

    DISABLE_LIQUIDITY_POOL_TRADING_FLAG = 1
    DISABLE_LIQUIDITY_POOL_DEPOSIT_FLAG = 2
    DISABLE_LIQUIDITY_POOL_WITHDRAWAL_FLAG = 4

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> LedgerHeaderFlags:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerHeaderFlags:
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
    def from_xdr(cls, xdr: str) -> LedgerHeaderFlags:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LedgerHeaderFlags:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _LEDGER_HEADER_FLAGS_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> LedgerHeaderFlags:
        return cls(_LEDGER_HEADER_FLAGS_REVERSE_MAP[json_value])
