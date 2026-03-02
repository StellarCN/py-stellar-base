# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
        constant_product: Optional[LiquidityPoolConstantProductParameters] = None,
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
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> LiquidityPoolParameters:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = LiquidityPoolType.unpack(unpacker)
        if type == LiquidityPoolType.LIQUIDITY_POOL_CONSTANT_PRODUCT:
            constant_product = LiquidityPoolConstantProductParameters.unpack(
                unpacker, depth_limit - 1
            )
            return cls(type=type, constant_product=constant_product)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LiquidityPoolParameters:
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
    def from_xdr(cls, xdr: str) -> LiquidityPoolParameters:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LiquidityPoolParameters:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.type == LiquidityPoolType.LIQUIDITY_POOL_CONSTANT_PRODUCT:
            assert self.constant_product is not None
            return {
                "liquidity_pool_constant_product": self.constant_product.to_json_dict()
            }
        raise ValueError(f"Unknown type in LiquidityPoolParameters: {self.type}")

    @classmethod
    def from_json_dict(cls, json_value: dict) -> LiquidityPoolParameters:
        if len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for LiquidityPoolParameters, got: {json_value}"
            )
        key = next(iter(json_value))
        type = LiquidityPoolType.from_json_dict(key)
        if key == "liquidity_pool_constant_product":
            constant_product = LiquidityPoolConstantProductParameters.from_json_dict(
                json_value["liquidity_pool_constant_product"]
            )
            return cls(type=type, constant_product=constant_product)
        raise ValueError(f"Unknown key '{key}' for LiquidityPoolParameters")

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
        if self.constant_product is not None:
            out.append(f"constant_product={self.constant_product}")
        return f"<LiquidityPoolParameters [{', '.join(out)}]>"
