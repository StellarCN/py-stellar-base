# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .liquidity_pool_withdraw_result_code import LiquidityPoolWithdrawResultCode

__all__ = ["LiquidityPoolWithdrawResult"]


class LiquidityPoolWithdrawResult:
    """
    XDR Source Code::

        union LiquidityPoolWithdrawResult switch (LiquidityPoolWithdrawResultCode code)
        {
        case LIQUIDITY_POOL_WITHDRAW_SUCCESS:
            void;
        case LIQUIDITY_POOL_WITHDRAW_MALFORMED:
        case LIQUIDITY_POOL_WITHDRAW_NO_TRUST:
        case LIQUIDITY_POOL_WITHDRAW_UNDERFUNDED:
        case LIQUIDITY_POOL_WITHDRAW_LINE_FULL:
        case LIQUIDITY_POOL_WITHDRAW_UNDER_MINIMUM:
        case LIQUIDITY_POOL_WITHDRAW_TRUSTLINE_FROZEN:
            void;
        };
    """

    def __init__(
        self,
        code: LiquidityPoolWithdrawResultCode,
    ) -> None:
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == LiquidityPoolWithdrawResultCode.LIQUIDITY_POOL_WITHDRAW_SUCCESS:
            return
        if (
            self.code
            == LiquidityPoolWithdrawResultCode.LIQUIDITY_POOL_WITHDRAW_MALFORMED
        ):
            return
        if (
            self.code
            == LiquidityPoolWithdrawResultCode.LIQUIDITY_POOL_WITHDRAW_NO_TRUST
        ):
            return
        if (
            self.code
            == LiquidityPoolWithdrawResultCode.LIQUIDITY_POOL_WITHDRAW_UNDERFUNDED
        ):
            return
        if (
            self.code
            == LiquidityPoolWithdrawResultCode.LIQUIDITY_POOL_WITHDRAW_LINE_FULL
        ):
            return
        if (
            self.code
            == LiquidityPoolWithdrawResultCode.LIQUIDITY_POOL_WITHDRAW_UNDER_MINIMUM
        ):
            return
        if (
            self.code
            == LiquidityPoolWithdrawResultCode.LIQUIDITY_POOL_WITHDRAW_TRUSTLINE_FROZEN
        ):
            return
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> LiquidityPoolWithdrawResult:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        code = LiquidityPoolWithdrawResultCode.unpack(unpacker)
        if code == LiquidityPoolWithdrawResultCode.LIQUIDITY_POOL_WITHDRAW_SUCCESS:
            return cls(code=code)
        if code == LiquidityPoolWithdrawResultCode.LIQUIDITY_POOL_WITHDRAW_MALFORMED:
            return cls(code=code)
        if code == LiquidityPoolWithdrawResultCode.LIQUIDITY_POOL_WITHDRAW_NO_TRUST:
            return cls(code=code)
        if code == LiquidityPoolWithdrawResultCode.LIQUIDITY_POOL_WITHDRAW_UNDERFUNDED:
            return cls(code=code)
        if code == LiquidityPoolWithdrawResultCode.LIQUIDITY_POOL_WITHDRAW_LINE_FULL:
            return cls(code=code)
        if (
            code
            == LiquidityPoolWithdrawResultCode.LIQUIDITY_POOL_WITHDRAW_UNDER_MINIMUM
        ):
            return cls(code=code)
        if (
            code
            == LiquidityPoolWithdrawResultCode.LIQUIDITY_POOL_WITHDRAW_TRUSTLINE_FROZEN
        ):
            return cls(code=code)
        raise ValueError("Invalid code.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LiquidityPoolWithdrawResult:
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
    def from_xdr(cls, xdr: str) -> LiquidityPoolWithdrawResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LiquidityPoolWithdrawResult:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.code == LiquidityPoolWithdrawResultCode.LIQUIDITY_POOL_WITHDRAW_SUCCESS:
            return "success"
        if (
            self.code
            == LiquidityPoolWithdrawResultCode.LIQUIDITY_POOL_WITHDRAW_MALFORMED
        ):
            return "malformed"
        if (
            self.code
            == LiquidityPoolWithdrawResultCode.LIQUIDITY_POOL_WITHDRAW_NO_TRUST
        ):
            return "no_trust"
        if (
            self.code
            == LiquidityPoolWithdrawResultCode.LIQUIDITY_POOL_WITHDRAW_UNDERFUNDED
        ):
            return "underfunded"
        if (
            self.code
            == LiquidityPoolWithdrawResultCode.LIQUIDITY_POOL_WITHDRAW_LINE_FULL
        ):
            return "line_full"
        if (
            self.code
            == LiquidityPoolWithdrawResultCode.LIQUIDITY_POOL_WITHDRAW_UNDER_MINIMUM
        ):
            return "under_minimum"
        if (
            self.code
            == LiquidityPoolWithdrawResultCode.LIQUIDITY_POOL_WITHDRAW_TRUSTLINE_FROZEN
        ):
            return "trustline_frozen"
        raise ValueError(f"Unknown code in LiquidityPoolWithdrawResult: {self.code}")

    @classmethod
    def from_json_dict(cls, json_value: str) -> LiquidityPoolWithdrawResult:
        if json_value not in (
            "success",
            "malformed",
            "no_trust",
            "underfunded",
            "line_full",
            "under_minimum",
            "trustline_frozen",
        ):
            raise ValueError(
                f"Unexpected string '{json_value}' for LiquidityPoolWithdrawResult, must be one of: success, malformed, no_trust, underfunded, line_full, under_minimum, trustline_frozen"
            )
        code = LiquidityPoolWithdrawResultCode.from_json_dict(json_value)
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
        return f"<LiquidityPoolWithdrawResult [{', '.join(out)}]>"
