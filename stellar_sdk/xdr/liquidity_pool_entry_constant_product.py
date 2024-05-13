# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .int64 import Int64
from .liquidity_pool_constant_product_parameters import (
    LiquidityPoolConstantProductParameters,
)

__all__ = ["LiquidityPoolEntryConstantProduct"]


class LiquidityPoolEntryConstantProduct:
    """
    XDR Source Code::

        struct
                {
                    LiquidityPoolConstantProductParameters params;

                    int64 reserveA;        // amount of A in the pool
                    int64 reserveB;        // amount of B in the pool
                    int64 totalPoolShares; // total number of pool shares issued
                    int64 poolSharesTrustLineCount; // number of trust lines for the
                                                    // associated pool shares
                }
    """

    def __init__(
        self,
        params: LiquidityPoolConstantProductParameters,
        reserve_a: Int64,
        reserve_b: Int64,
        total_pool_shares: Int64,
        pool_shares_trust_line_count: Int64,
    ) -> None:
        self.params = params
        self.reserve_a = reserve_a
        self.reserve_b = reserve_b
        self.total_pool_shares = total_pool_shares
        self.pool_shares_trust_line_count = pool_shares_trust_line_count

    def pack(self, packer: Packer) -> None:
        self.params.pack(packer)
        self.reserve_a.pack(packer)
        self.reserve_b.pack(packer)
        self.total_pool_shares.pack(packer)
        self.pool_shares_trust_line_count.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> LiquidityPoolEntryConstantProduct:
        params = LiquidityPoolConstantProductParameters.unpack(unpacker)
        reserve_a = Int64.unpack(unpacker)
        reserve_b = Int64.unpack(unpacker)
        total_pool_shares = Int64.unpack(unpacker)
        pool_shares_trust_line_count = Int64.unpack(unpacker)
        return cls(
            params=params,
            reserve_a=reserve_a,
            reserve_b=reserve_b,
            total_pool_shares=total_pool_shares,
            pool_shares_trust_line_count=pool_shares_trust_line_count,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LiquidityPoolEntryConstantProduct:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LiquidityPoolEntryConstantProduct:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.params,
                self.reserve_a,
                self.reserve_b,
                self.total_pool_shares,
                self.pool_shares_trust_line_count,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.params == other.params
            and self.reserve_a == other.reserve_a
            and self.reserve_b == other.reserve_b
            and self.total_pool_shares == other.total_pool_shares
            and self.pool_shares_trust_line_count == other.pool_shares_trust_line_count
        )

    def __repr__(self):
        out = [
            f"params={self.params}",
            f"reserve_a={self.reserve_a}",
            f"reserve_b={self.reserve_b}",
            f"total_pool_shares={self.total_pool_shares}",
            f"pool_shares_trust_line_count={self.pool_shares_trust_line_count}",
        ]
        return f"<LiquidityPoolEntryConstantProduct [{', '.join(out)}]>"
