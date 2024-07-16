# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .liquidity_pool_constant_product_parameters import (
    LiquidityPoolConstantProductParameters,
)
from .liquidity_pool_type import LiquidityPoolType

__all__ = ["LiquidityPoolParameters"]


class LiquidityPoolParameters:
    """
    XDR Source Code::

        union LiquidityPoolParameters switch (LiquidityPoolType type)
        {
        case LIQUIDITY_POOL_CONSTANT_PRODUCT:
            LiquidityPoolConstantProductParameters constantProduct;
        };
    """

    def __init__(
        self,
        type: LiquidityPoolType,
        constant_product: LiquidityPoolConstantProductParameters = None,
    ) -> None:
        self.type = type
        self.constant_product = constant_product

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == LiquidityPoolType.LIQUIDITY_POOL_CONSTANT_PRODUCT:
            if self.constant_product is None:
                raise ValueError("constant_product should not be None.")
            self.constant_product.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> LiquidityPoolParameters:
        type = LiquidityPoolType.unpack(unpacker)
        if type == LiquidityPoolType.LIQUIDITY_POOL_CONSTANT_PRODUCT:
            constant_product = LiquidityPoolConstantProductParameters.unpack(unpacker)
            return cls(type=type, constant_product=constant_product)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LiquidityPoolParameters:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LiquidityPoolParameters:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.type,
                self.constant_product,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type and self.constant_product == other.constant_product
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        (
            out.append(f"constant_product={self.constant_product}")
            if self.constant_product is not None
            else None
        )
        return f"<LiquidityPoolParameters [{', '.join(out)}]>"
