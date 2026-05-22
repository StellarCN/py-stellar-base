# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_LIQUIDITY_POOL_DEPOSIT_RESULT_CODE_MAP = {
    0: "success",
    -1: "malformed",
    -2: "no_trust",
    -3: "not_authorized",
    -4: "underfunded",
    -5: "line_full",
    -6: "bad_price",
    -7: "pool_full",
    -8: "trustline_frozen",
}
_LIQUIDITY_POOL_DEPOSIT_RESULT_CODE_REVERSE_MAP = {
    "success": 0,
    "malformed": -1,
    "no_trust": -2,
    "not_authorized": -3,
    "underfunded": -4,
    "line_full": -5,
    "bad_price": -6,
    "pool_full": -7,
    "trustline_frozen": -8,
}
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
            LIQUIDITY_POOL_DEPOSIT_POOL_FULL = -7,      // pool reserves are full
            LIQUIDITY_POOL_DEPOSIT_TRUSTLINE_FROZEN = -8  // trustline for one of the
                                                          // assets is frozen
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
    LIQUIDITY_POOL_DEPOSIT_TRUSTLINE_FROZEN = -8

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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LiquidityPoolDepositResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LiquidityPoolDepositResultCode:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _LIQUIDITY_POOL_DEPOSIT_RESULT_CODE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> LiquidityPoolDepositResultCode:
        return cls(_LIQUIDITY_POOL_DEPOSIT_RESULT_CODE_REVERSE_MAP[json_value])
