# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .alpha_num4 import AlphaNum4
from .alpha_num12 import AlphaNum12
from .asset_type import AssetType
from .liquidity_pool_parameters import LiquidityPoolParameters

__all__ = ["ChangeTrustAsset"]


class ChangeTrustAsset:
    """
    XDR Source Code::

        union ChangeTrustAsset switch (AssetType type)
        {
        case ASSET_TYPE_NATIVE: // Not credit
            void;

        case ASSET_TYPE_CREDIT_ALPHANUM4:
            AlphaNum4 alphaNum4;

        case ASSET_TYPE_CREDIT_ALPHANUM12:
            AlphaNum12 alphaNum12;

        case ASSET_TYPE_POOL_SHARE:
            LiquidityPoolParameters liquidityPool;

            // add other asset types here in the future
        };
    """

    def __init__(
        self,
        type: AssetType,
        alpha_num4: AlphaNum4 = None,
        alpha_num12: AlphaNum12 = None,
        liquidity_pool: LiquidityPoolParameters = None,
    ) -> None:
        self.type = type
        self.alpha_num4 = alpha_num4
        self.alpha_num12 = alpha_num12
        self.liquidity_pool = liquidity_pool

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == AssetType.ASSET_TYPE_NATIVE:
            return
        if self.type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM4:
            if self.alpha_num4 is None:
                raise ValueError("alpha_num4 should not be None.")
            self.alpha_num4.pack(packer)
            return
        if self.type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM12:
            if self.alpha_num12 is None:
                raise ValueError("alpha_num12 should not be None.")
            self.alpha_num12.pack(packer)
            return
        if self.type == AssetType.ASSET_TYPE_POOL_SHARE:
            if self.liquidity_pool is None:
                raise ValueError("liquidity_pool should not be None.")
            self.liquidity_pool.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ChangeTrustAsset:
        type = AssetType.unpack(unpacker)
        if type == AssetType.ASSET_TYPE_NATIVE:
            return cls(type=type)
        if type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM4:
            alpha_num4 = AlphaNum4.unpack(unpacker)
            return cls(type=type, alpha_num4=alpha_num4)
        if type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM12:
            alpha_num12 = AlphaNum12.unpack(unpacker)
            return cls(type=type, alpha_num12=alpha_num12)
        if type == AssetType.ASSET_TYPE_POOL_SHARE:
            liquidity_pool = LiquidityPoolParameters.unpack(unpacker)
            return cls(type=type, liquidity_pool=liquidity_pool)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ChangeTrustAsset:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ChangeTrustAsset:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.type,
                self.alpha_num4,
                self.alpha_num12,
                self.liquidity_pool,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.alpha_num4 == other.alpha_num4
            and self.alpha_num12 == other.alpha_num12
            and self.liquidity_pool == other.liquidity_pool
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        (
            out.append(f"alpha_num4={self.alpha_num4}")
            if self.alpha_num4 is not None
            else None
        )
        (
            out.append(f"alpha_num12={self.alpha_num12}")
            if self.alpha_num12 is not None
            else None
        )
        (
            out.append(f"liquidity_pool={self.liquidity_pool}")
            if self.liquidity_pool is not None
            else None
        )
        return f"<ChangeTrustAsset [{', '.join(out)}]>"
