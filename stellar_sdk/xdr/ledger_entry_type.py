# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

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
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LedgerEntryType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
