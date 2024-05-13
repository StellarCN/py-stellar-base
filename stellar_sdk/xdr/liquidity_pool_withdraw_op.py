# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .int64 import Int64
from .pool_id import PoolID

__all__ = ["LiquidityPoolWithdrawOp"]


class LiquidityPoolWithdrawOp:
    """
    XDR Source Code::

        struct LiquidityPoolWithdrawOp
        {
            PoolID liquidityPoolID;
            int64 amount;     // amount of pool shares to withdraw
            int64 minAmountA; // minimum amount of first asset to withdraw
            int64 minAmountB; // minimum amount of second asset to withdraw
        };
    """

    def __init__(
        self,
        liquidity_pool_id: PoolID,
        amount: Int64,
        min_amount_a: Int64,
        min_amount_b: Int64,
    ) -> None:
        self.liquidity_pool_id = liquidity_pool_id
        self.amount = amount
        self.min_amount_a = min_amount_a
        self.min_amount_b = min_amount_b

    def pack(self, packer: Packer) -> None:
        self.liquidity_pool_id.pack(packer)
        self.amount.pack(packer)
        self.min_amount_a.pack(packer)
        self.min_amount_b.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> LiquidityPoolWithdrawOp:
        liquidity_pool_id = PoolID.unpack(unpacker)
        amount = Int64.unpack(unpacker)
        min_amount_a = Int64.unpack(unpacker)
        min_amount_b = Int64.unpack(unpacker)
        return cls(
            liquidity_pool_id=liquidity_pool_id,
            amount=amount,
            min_amount_a=min_amount_a,
            min_amount_b=min_amount_b,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LiquidityPoolWithdrawOp:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LiquidityPoolWithdrawOp:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.liquidity_pool_id,
                self.amount,
                self.min_amount_a,
                self.min_amount_b,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.liquidity_pool_id == other.liquidity_pool_id
            and self.amount == other.amount
            and self.min_amount_a == other.min_amount_a
            and self.min_amount_b == other.min_amount_b
        )

    def __repr__(self):
        out = [
            f"liquidity_pool_id={self.liquidity_pool_id}",
            f"amount={self.amount}",
            f"min_amount_a={self.min_amount_a}",
            f"min_amount_b={self.min_amount_b}",
        ]
        return f"<LiquidityPoolWithdrawOp [{', '.join(out)}]>"
