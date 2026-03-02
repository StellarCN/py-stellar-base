# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .liquidity_pool_deposit_result_code import LiquidityPoolDepositResultCode

__all__ = ["LiquidityPoolDepositResult"]


class LiquidityPoolDepositResult:
    """
    XDR Source Code::

        union LiquidityPoolDepositResult switch (LiquidityPoolDepositResultCode code)
        {
        case LIQUIDITY_POOL_DEPOSIT_SUCCESS:
            void;
        case LIQUIDITY_POOL_DEPOSIT_MALFORMED:
        case LIQUIDITY_POOL_DEPOSIT_NO_TRUST:
        case LIQUIDITY_POOL_DEPOSIT_NOT_AUTHORIZED:
        case LIQUIDITY_POOL_DEPOSIT_UNDERFUNDED:
        case LIQUIDITY_POOL_DEPOSIT_LINE_FULL:
        case LIQUIDITY_POOL_DEPOSIT_BAD_PRICE:
        case LIQUIDITY_POOL_DEPOSIT_POOL_FULL:
            void;
        };
    """

    def __init__(
        self,
        code: LiquidityPoolDepositResultCode,
    ) -> None:
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == LiquidityPoolDepositResultCode.LIQUIDITY_POOL_DEPOSIT_SUCCESS:
            return
        if self.code == LiquidityPoolDepositResultCode.LIQUIDITY_POOL_DEPOSIT_MALFORMED:
            return
        if self.code == LiquidityPoolDepositResultCode.LIQUIDITY_POOL_DEPOSIT_NO_TRUST:
            return
        if (
            self.code
            == LiquidityPoolDepositResultCode.LIQUIDITY_POOL_DEPOSIT_NOT_AUTHORIZED
        ):
            return
        if (
            self.code
            == LiquidityPoolDepositResultCode.LIQUIDITY_POOL_DEPOSIT_UNDERFUNDED
        ):
            return
        if self.code == LiquidityPoolDepositResultCode.LIQUIDITY_POOL_DEPOSIT_LINE_FULL:
            return
        if self.code == LiquidityPoolDepositResultCode.LIQUIDITY_POOL_DEPOSIT_BAD_PRICE:
            return
        if self.code == LiquidityPoolDepositResultCode.LIQUIDITY_POOL_DEPOSIT_POOL_FULL:
            return
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> LiquidityPoolDepositResult:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        code = LiquidityPoolDepositResultCode.unpack(unpacker)
        if code == LiquidityPoolDepositResultCode.LIQUIDITY_POOL_DEPOSIT_SUCCESS:
            return cls(code=code)
        if code == LiquidityPoolDepositResultCode.LIQUIDITY_POOL_DEPOSIT_MALFORMED:
            return cls(code=code)
        if code == LiquidityPoolDepositResultCode.LIQUIDITY_POOL_DEPOSIT_NO_TRUST:
            return cls(code=code)
        if code == LiquidityPoolDepositResultCode.LIQUIDITY_POOL_DEPOSIT_NOT_AUTHORIZED:
            return cls(code=code)
        if code == LiquidityPoolDepositResultCode.LIQUIDITY_POOL_DEPOSIT_UNDERFUNDED:
            return cls(code=code)
        if code == LiquidityPoolDepositResultCode.LIQUIDITY_POOL_DEPOSIT_LINE_FULL:
            return cls(code=code)
        if code == LiquidityPoolDepositResultCode.LIQUIDITY_POOL_DEPOSIT_BAD_PRICE:
            return cls(code=code)
        if code == LiquidityPoolDepositResultCode.LIQUIDITY_POOL_DEPOSIT_POOL_FULL:
            return cls(code=code)
        raise ValueError("Invalid code.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LiquidityPoolDepositResult:
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
    def from_xdr(cls, xdr: str) -> LiquidityPoolDepositResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LiquidityPoolDepositResult:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.code == LiquidityPoolDepositResultCode.LIQUIDITY_POOL_DEPOSIT_SUCCESS:
            return "success"
        if self.code == LiquidityPoolDepositResultCode.LIQUIDITY_POOL_DEPOSIT_MALFORMED:
            return "malformed"
        if self.code == LiquidityPoolDepositResultCode.LIQUIDITY_POOL_DEPOSIT_NO_TRUST:
            return "no_trust"
        if (
            self.code
            == LiquidityPoolDepositResultCode.LIQUIDITY_POOL_DEPOSIT_NOT_AUTHORIZED
        ):
            return "not_authorized"
        if (
            self.code
            == LiquidityPoolDepositResultCode.LIQUIDITY_POOL_DEPOSIT_UNDERFUNDED
        ):
            return "underfunded"
        if self.code == LiquidityPoolDepositResultCode.LIQUIDITY_POOL_DEPOSIT_LINE_FULL:
            return "line_full"
        if self.code == LiquidityPoolDepositResultCode.LIQUIDITY_POOL_DEPOSIT_BAD_PRICE:
            return "bad_price"
        if self.code == LiquidityPoolDepositResultCode.LIQUIDITY_POOL_DEPOSIT_POOL_FULL:
            return "pool_full"
        raise ValueError(f"Unknown code in LiquidityPoolDepositResult: {self.code}")

    @classmethod
    def from_json_dict(cls, json_value: str) -> LiquidityPoolDepositResult:
        if json_value not in (
            "success",
            "malformed",
            "no_trust",
            "not_authorized",
            "underfunded",
            "line_full",
            "bad_price",
            "pool_full",
        ):
            raise ValueError(
                f"Unexpected string '{json_value}' for LiquidityPoolDepositResult, must be one of: success, malformed, no_trust, not_authorized, underfunded, line_full, bad_price, pool_full"
            )
        code = LiquidityPoolDepositResultCode.from_json_dict(json_value)
        return cls(code=code)

    def __hash__(self):
        return hash((self.code,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code

    def __repr__(self):
        out = []
        out.append(f"code={self.code}")
        return f"<LiquidityPoolDepositResult [{', '.join(out)}]>"
