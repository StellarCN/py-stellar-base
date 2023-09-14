# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

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
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LedgerUpgradeType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
