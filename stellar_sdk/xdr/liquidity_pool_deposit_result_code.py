# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

__all__ = ["LiquidityPoolDepositResultCode"]


class LiquidityPoolDepositResultCode(IntEnum):
    """
    XDR Source Code::

        enum LiquidityPoolDepositResultCode
        {
            // codes considered as "success" for the operation
            LIQUIDITY_POOL_DEPOSIT_SUCCESS = 0,

            // codes considered as "failure" for the operation
            LIQUIDITY_POOL_DEPOSIT_MALFORMED = -1,      // bad input
            LIQUIDITY_POOL_DEPOSIT_NO_TRUST = -2,       // no trust line for one of the
                                                        // assets
            LIQUIDITY_POOL_DEPOSIT_NOT_AUTHORIZED = -3, // not authorized for one of the
                                                        // assets
            LIQUIDITY_POOL_DEPOSIT_UNDERFUNDED = -4,    // not enough balance for one of
                                                        // the assets
            LIQUIDITY_POOL_DEPOSIT_LINE_FULL = -5,      // pool share trust line doesn't
                                                        // have sufficient limit
            LIQUIDITY_POOL_DEPOSIT_BAD_PRICE = -6,      // deposit price outside bounds
            LIQUIDITY_POOL_DEPOSIT_POOL_FULL = -7       // pool reserves are full
        };
    """

    LIQUIDITY_POOL_DEPOSIT_SUCCESS = 0
    LIQUIDITY_POOL_DEPOSIT_MALFORMED = -1
    LIQUIDITY_POOL_DEPOSIT_NO_TRUST = -2
    LIQUIDITY_POOL_DEPOSIT_NOT_AUTHORIZED = -3
    LIQUIDITY_POOL_DEPOSIT_UNDERFUNDED = -4
    LIQUIDITY_POOL_DEPOSIT_LINE_FULL = -5
    LIQUIDITY_POOL_DEPOSIT_BAD_PRICE = -6
    LIQUIDITY_POOL_DEPOSIT_POOL_FULL = -7

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> LiquidityPoolDepositResultCode:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LiquidityPoolDepositResultCode:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LiquidityPoolDepositResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
