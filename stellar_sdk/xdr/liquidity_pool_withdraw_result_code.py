# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_LIQUIDITY_POOL_WITHDRAW_RESULT_CODE_MAP = {
    0: "success",
    -1: "malformed",
    -2: "no_trust",
    -3: "underfunded",
    -4: "line_full",
    -5: "under_minimum",
}
_LIQUIDITY_POOL_WITHDRAW_RESULT_CODE_REVERSE_MAP = {
    "success": 0,
    "malformed": -1,
    "no_trust": -2,
    "underfunded": -3,
    "line_full": -4,
    "under_minimum": -5,
}
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LiquidityPoolWithdrawResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LiquidityPoolWithdrawResultCode:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _LIQUIDITY_POOL_WITHDRAW_RESULT_CODE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> LiquidityPoolWithdrawResultCode:
        return cls(_LIQUIDITY_POOL_WITHDRAW_RESULT_CODE_REVERSE_MAP[json_value])
