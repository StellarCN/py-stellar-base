# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .pool_id import PoolID

__all__ = ["LedgerKeyLiquidityPool"]


class LedgerKeyLiquidityPool:
    """
    XDR Source Code::

        struct
            {
                PoolID liquidityPoolID;
            }
    """

    def __init__(
        self,
        liquidity_pool_id: PoolID,
    ) -> None:
        self.liquidity_pool_id = liquidity_pool_id

    def pack(self, packer: Packer) -> None:
        self.liquidity_pool_id.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> LedgerKeyLiquidityPool:
        liquidity_pool_id = PoolID.unpack(unpacker)
        return cls(
            liquidity_pool_id=liquidity_pool_id,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerKeyLiquidityPool:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LedgerKeyLiquidityPool:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash((self.liquidity_pool_id,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.liquidity_pool_id == other.liquidity_pool_id

    def __repr__(self):
        out = [
            f"liquidity_pool_id={self.liquidity_pool_id}",
        ]
        return f"<LedgerKeyLiquidityPool [{', '.join(out)}]>"
