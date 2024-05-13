# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .asset import Asset
from .int64 import Int64
from .pool_id import PoolID

__all__ = ["ClaimLiquidityAtom"]


class ClaimLiquidityAtom:
    """
    XDR Source Code::

        struct ClaimLiquidityAtom
        {
            PoolID liquidityPoolID;

            // amount and asset taken from the pool
            Asset assetSold;
            int64 amountSold;

            // amount and asset sent to the pool
            Asset assetBought;
            int64 amountBought;
        };
    """

    def __init__(
        self,
        liquidity_pool_id: PoolID,
        asset_sold: Asset,
        amount_sold: Int64,
        asset_bought: Asset,
        amount_bought: Int64,
    ) -> None:
        self.liquidity_pool_id = liquidity_pool_id
        self.asset_sold = asset_sold
        self.amount_sold = amount_sold
        self.asset_bought = asset_bought
        self.amount_bought = amount_bought

    def pack(self, packer: Packer) -> None:
        self.liquidity_pool_id.pack(packer)
        self.asset_sold.pack(packer)
        self.amount_sold.pack(packer)
        self.asset_bought.pack(packer)
        self.amount_bought.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ClaimLiquidityAtom:
        liquidity_pool_id = PoolID.unpack(unpacker)
        asset_sold = Asset.unpack(unpacker)
        amount_sold = Int64.unpack(unpacker)
        asset_bought = Asset.unpack(unpacker)
        amount_bought = Int64.unpack(unpacker)
        return cls(
            liquidity_pool_id=liquidity_pool_id,
            asset_sold=asset_sold,
            amount_sold=amount_sold,
            asset_bought=asset_bought,
            amount_bought=amount_bought,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ClaimLiquidityAtom:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ClaimLiquidityAtom:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.liquidity_pool_id,
                self.asset_sold,
                self.amount_sold,
                self.asset_bought,
                self.amount_bought,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.liquidity_pool_id == other.liquidity_pool_id
            and self.asset_sold == other.asset_sold
            and self.amount_sold == other.amount_sold
            and self.asset_bought == other.asset_bought
            and self.amount_bought == other.amount_bought
        )

    def __repr__(self):
        out = [
            f"liquidity_pool_id={self.liquidity_pool_id}",
            f"asset_sold={self.asset_sold}",
            f"amount_sold={self.amount_sold}",
            f"asset_bought={self.asset_bought}",
            f"amount_bought={self.amount_bought}",
        ]
        return f"<ClaimLiquidityAtom [{', '.join(out)}]>"
