# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .int64 import Int64
from .pool_id import PoolID
from .price import Price

__all__ = ["LiquidityPoolDepositOp"]


class LiquidityPoolDepositOp:
    """
    XDR Source Code::

        struct LiquidityPoolDepositOp
        {
            PoolID liquidityPoolID;
            int64 maxAmountA; // maximum amount of first asset to deposit
            int64 maxAmountB; // maximum amount of second asset to deposit
            Price minPrice;   // minimum depositA/depositB
            Price maxPrice;   // maximum depositA/depositB
        };
    """

    def __init__(
        self,
        liquidity_pool_id: PoolID,
        max_amount_a: Int64,
        max_amount_b: Int64,
        min_price: Price,
        max_price: Price,
    ) -> None:
        self.liquidity_pool_id = liquidity_pool_id
        self.max_amount_a = max_amount_a
        self.max_amount_b = max_amount_b
        self.min_price = min_price
        self.max_price = max_price

    def pack(self, packer: Packer) -> None:
        self.liquidity_pool_id.pack(packer)
        self.max_amount_a.pack(packer)
        self.max_amount_b.pack(packer)
        self.min_price.pack(packer)
        self.max_price.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> LiquidityPoolDepositOp:
        liquidity_pool_id = PoolID.unpack(unpacker)
        max_amount_a = Int64.unpack(unpacker)
        max_amount_b = Int64.unpack(unpacker)
        min_price = Price.unpack(unpacker)
        max_price = Price.unpack(unpacker)
        return cls(
            liquidity_pool_id=liquidity_pool_id,
            max_amount_a=max_amount_a,
            max_amount_b=max_amount_b,
            min_price=min_price,
            max_price=max_price,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LiquidityPoolDepositOp:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LiquidityPoolDepositOp:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.liquidity_pool_id,
                self.max_amount_a,
                self.max_amount_b,
                self.min_price,
                self.max_price,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.liquidity_pool_id == other.liquidity_pool_id
            and self.max_amount_a == other.max_amount_a
            and self.max_amount_b == other.max_amount_b
            and self.min_price == other.min_price
            and self.max_price == other.max_price
        )

    def __repr__(self):
        out = [
            f"liquidity_pool_id={self.liquidity_pool_id}",
            f"max_amount_a={self.max_amount_a}",
            f"max_amount_b={self.max_amount_b}",
            f"min_price={self.min_price}",
            f"max_price={self.max_price}",
        ]
        return f"<LiquidityPoolDepositOp [{', '.join(out)}]>"
