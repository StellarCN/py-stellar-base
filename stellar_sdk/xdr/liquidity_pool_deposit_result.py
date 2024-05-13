# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

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

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> LiquidityPoolDepositResult:
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
        return cls(code=code)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LiquidityPoolDepositResult:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LiquidityPoolDepositResult:
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
        return f"<LiquidityPoolDepositResult [{', '.join(out)}]>"
