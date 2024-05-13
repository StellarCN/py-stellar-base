# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .liquidity_pool_entry_body import LiquidityPoolEntryBody
from .pool_id import PoolID

__all__ = ["LiquidityPoolEntry"]


class LiquidityPoolEntry:
    """
    XDR Source Code::

        struct LiquidityPoolEntry
        {
            PoolID liquidityPoolID;

            union switch (LiquidityPoolType type)
            {
            case LIQUIDITY_POOL_CONSTANT_PRODUCT:
                struct
                {
                    LiquidityPoolConstantProductParameters params;

                    int64 reserveA;        // amount of A in the pool
                    int64 reserveB;        // amount of B in the pool
                    int64 totalPoolShares; // total number of pool shares issued
                    int64 poolSharesTrustLineCount; // number of trust lines for the
                                                    // associated pool shares
                } constantProduct;
            }
            body;
        };
    """

    def __init__(
        self,
        liquidity_pool_id: PoolID,
        body: LiquidityPoolEntryBody,
    ) -> None:
        self.liquidity_pool_id = liquidity_pool_id
        self.body = body

    def pack(self, packer: Packer) -> None:
        self.liquidity_pool_id.pack(packer)
        self.body.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> LiquidityPoolEntry:
        liquidity_pool_id = PoolID.unpack(unpacker)
        body = LiquidityPoolEntryBody.unpack(unpacker)
        return cls(
            liquidity_pool_id=liquidity_pool_id,
            body=body,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LiquidityPoolEntry:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LiquidityPoolEntry:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.liquidity_pool_id,
                self.body,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.liquidity_pool_id == other.liquidity_pool_id
            and self.body == other.body
        )

    def __repr__(self):
        out = [
            f"liquidity_pool_id={self.liquidity_pool_id}",
            f"body={self.body}",
        ]
        return f"<LiquidityPoolEntry [{', '.join(out)}]>"
