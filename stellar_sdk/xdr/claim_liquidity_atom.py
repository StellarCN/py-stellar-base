# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .asset import Asset
from .base import DEFAULT_XDR_MAX_DEPTH
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ClaimLiquidityAtom:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        liquidity_pool_id = PoolID.unpack(unpacker, depth_limit - 1)
        asset_sold = Asset.unpack(unpacker, depth_limit - 1)
        amount_sold = Int64.unpack(unpacker, depth_limit - 1)
        asset_bought = Asset.unpack(unpacker, depth_limit - 1)
        amount_bought = Int64.unpack(unpacker, depth_limit - 1)
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ClaimLiquidityAtom:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ClaimLiquidityAtom:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "liquidity_pool_id": self.liquidity_pool_id.to_json_dict(),
            "asset_sold": self.asset_sold.to_json_dict(),
            "amount_sold": self.amount_sold.to_json_dict(),
            "asset_bought": self.asset_bought.to_json_dict(),
            "amount_bought": self.amount_bought.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> ClaimLiquidityAtom:
        liquidity_pool_id = PoolID.from_json_dict(json_dict["liquidity_pool_id"])
        asset_sold = Asset.from_json_dict(json_dict["asset_sold"])
        amount_sold = Int64.from_json_dict(json_dict["amount_sold"])
        asset_bought = Asset.from_json_dict(json_dict["asset_bought"])
        amount_bought = Int64.from_json_dict(json_dict["amount_bought"])
        return cls(
            liquidity_pool_id=liquidity_pool_id,
            asset_sold=asset_sold,
            amount_sold=amount_sold,
            asset_bought=asset_bought,
            amount_bought=amount_bought,
        )

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
