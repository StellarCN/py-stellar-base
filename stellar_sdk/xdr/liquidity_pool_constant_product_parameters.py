# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .asset import Asset
from .int32 import Int32

__all__ = ["LiquidityPoolConstantProductParameters"]


class LiquidityPoolConstantProductParameters:
    """
    XDR Source Code::

        struct LiquidityPoolConstantProductParameters
        {
            Asset assetA; // assetA < assetB
            Asset assetB;
            int32 fee; // Fee is in basis points, so the actual rate is (fee/100)%
        };
    """

    def __init__(
        self,
        asset_a: Asset,
        asset_b: Asset,
        fee: Int32,
    ) -> None:
        self.asset_a = asset_a
        self.asset_b = asset_b
        self.fee = fee

    def pack(self, packer: Packer) -> None:
        self.asset_a.pack(packer)
        self.asset_b.pack(packer)
        self.fee.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> LiquidityPoolConstantProductParameters:
        asset_a = Asset.unpack(unpacker)
        asset_b = Asset.unpack(unpacker)
        fee = Int32.unpack(unpacker)
        return cls(
            asset_a=asset_a,
            asset_b=asset_b,
            fee=fee,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LiquidityPoolConstantProductParameters:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LiquidityPoolConstantProductParameters:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.asset_a,
                self.asset_b,
                self.fee,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.asset_a == other.asset_a
            and self.asset_b == other.asset_b
            and self.fee == other.fee
        )

    def __repr__(self):
        out = [
            f"asset_a={self.asset_a}",
            f"asset_b={self.asset_b}",
            f"fee={self.fee}",
        ]
        return f"<LiquidityPoolConstantProductParameters [{', '.join(out)}]>"
