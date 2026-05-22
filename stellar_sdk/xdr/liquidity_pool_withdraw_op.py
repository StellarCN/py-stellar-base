# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> LiquidityPoolWithdrawOp:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        liquidity_pool_id = PoolID.unpack(unpacker, depth_limit - 1)
        amount = Int64.unpack(unpacker, depth_limit - 1)
        min_amount_a = Int64.unpack(unpacker, depth_limit - 1)
        min_amount_b = Int64.unpack(unpacker, depth_limit - 1)
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LiquidityPoolWithdrawOp:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LiquidityPoolWithdrawOp:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "liquidity_pool_id": self.liquidity_pool_id.to_json_dict(),
            "amount": self.amount.to_json_dict(),
            "min_amount_a": self.min_amount_a.to_json_dict(),
            "min_amount_b": self.min_amount_b.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> LiquidityPoolWithdrawOp:
        liquidity_pool_id = PoolID.from_json_dict(json_dict["liquidity_pool_id"])
        amount = Int64.from_json_dict(json_dict["amount"])
        min_amount_a = Int64.from_json_dict(json_dict["min_amount_a"])
        min_amount_b = Int64.from_json_dict(json_dict["min_amount_b"])
        return cls(
            liquidity_pool_id=liquidity_pool_id,
            amount=amount,
            min_amount_a=min_amount_a,
            min_amount_b=min_amount_b,
        )

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
