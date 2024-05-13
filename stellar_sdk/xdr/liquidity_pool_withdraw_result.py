# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

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

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> LiquidityPoolWithdrawResult:
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
        return cls(code=code)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LiquidityPoolWithdrawResult:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LiquidityPoolWithdrawResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
