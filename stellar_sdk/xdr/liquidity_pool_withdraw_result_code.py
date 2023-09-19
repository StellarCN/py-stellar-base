# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

__all__ = ["LiquidityPoolWithdrawResultCode"]


class LiquidityPoolWithdrawResultCode(IntEnum):
    """
    XDR Source Code::

        enum LiquidityPoolWithdrawResultCode
        {
            // codes considered as "success" for the operation
            LIQUIDITY_POOL_WITHDRAW_SUCCESS = 0,

            // codes considered as "failure" for the operation
            LIQUIDITY_POOL_WITHDRAW_MALFORMED = -1,    // bad input
            LIQUIDITY_POOL_WITHDRAW_NO_TRUST = -2,     // no trust line for one of the
                                                       // assets
            LIQUIDITY_POOL_WITHDRAW_UNDERFUNDED = -3,  // not enough balance of the
                                                       // pool share
            LIQUIDITY_POOL_WITHDRAW_LINE_FULL = -4,    // would go above limit for one
                                                       // of the assets
            LIQUIDITY_POOL_WITHDRAW_UNDER_MINIMUM = -5 // didn't withdraw enough
        };
    """

    LIQUIDITY_POOL_WITHDRAW_SUCCESS = 0
    LIQUIDITY_POOL_WITHDRAW_MALFORMED = -1
    LIQUIDITY_POOL_WITHDRAW_NO_TRUST = -2
    LIQUIDITY_POOL_WITHDRAW_UNDERFUNDED = -3
    LIQUIDITY_POOL_WITHDRAW_LINE_FULL = -4
    LIQUIDITY_POOL_WITHDRAW_UNDER_MINIMUM = -5

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> LiquidityPoolWithdrawResultCode:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LiquidityPoolWithdrawResultCode:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LiquidityPoolWithdrawResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
