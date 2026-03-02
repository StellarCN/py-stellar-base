# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .claim_atom_type import ClaimAtomType
from .claim_liquidity_atom import ClaimLiquidityAtom
from .claim_offer_atom import ClaimOfferAtom
from .claim_offer_atom_v0 import ClaimOfferAtomV0

__all__ = ["ClaimAtom"]


class ClaimAtom:
    """
    XDR Source Code::

        union ClaimAtom switch (ClaimAtomType type)
        {
        case CLAIM_ATOM_TYPE_V0:
            ClaimOfferAtomV0 v0;
        case CLAIM_ATOM_TYPE_ORDER_BOOK:
            ClaimOfferAtom orderBook;
        case CLAIM_ATOM_TYPE_LIQUIDITY_POOL:
            ClaimLiquidityAtom liquidityPool;
        };
    """

    def __init__(
        self,
        type: ClaimAtomType,
        v0: Optional[ClaimOfferAtomV0] = None,
        order_book: Optional[ClaimOfferAtom] = None,
        liquidity_pool: Optional[ClaimLiquidityAtom] = None,
    ) -> None:
        self.type = type
        self.v0 = v0
        self.order_book = order_book
        self.liquidity_pool = liquidity_pool

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == ClaimAtomType.CLAIM_ATOM_TYPE_V0:
            if self.v0 is None:
                raise ValueError("v0 should not be None.")
            self.v0.pack(packer)
            return
        if self.type == ClaimAtomType.CLAIM_ATOM_TYPE_ORDER_BOOK:
            if self.order_book is None:
                raise ValueError("order_book should not be None.")
            self.order_book.pack(packer)
            return
        if self.type == ClaimAtomType.CLAIM_ATOM_TYPE_LIQUIDITY_POOL:
            if self.liquidity_pool is None:
                raise ValueError("liquidity_pool should not be None.")
            self.liquidity_pool.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ClaimAtom:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = ClaimAtomType.unpack(unpacker)
        if type == ClaimAtomType.CLAIM_ATOM_TYPE_V0:
            v0 = ClaimOfferAtomV0.unpack(unpacker, depth_limit - 1)
            return cls(type=type, v0=v0)
        if type == ClaimAtomType.CLAIM_ATOM_TYPE_ORDER_BOOK:
            order_book = ClaimOfferAtom.unpack(unpacker, depth_limit - 1)
            return cls(type=type, order_book=order_book)
        if type == ClaimAtomType.CLAIM_ATOM_TYPE_LIQUIDITY_POOL:
            liquidity_pool = ClaimLiquidityAtom.unpack(unpacker, depth_limit - 1)
            return cls(type=type, liquidity_pool=liquidity_pool)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ClaimAtom:
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
    def from_xdr(cls, xdr: str) -> ClaimAtom:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ClaimAtom:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.type == ClaimAtomType.CLAIM_ATOM_TYPE_V0:
            assert self.v0 is not None
            return {"v0": self.v0.to_json_dict()}
        if self.type == ClaimAtomType.CLAIM_ATOM_TYPE_ORDER_BOOK:
            assert self.order_book is not None
            return {"order_book": self.order_book.to_json_dict()}
        if self.type == ClaimAtomType.CLAIM_ATOM_TYPE_LIQUIDITY_POOL:
            assert self.liquidity_pool is not None
            return {"liquidity_pool": self.liquidity_pool.to_json_dict()}
        raise ValueError(f"Unknown type in ClaimAtom: {self.type}")

    @classmethod
    def from_json_dict(cls, json_value: dict) -> ClaimAtom:
        if len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for ClaimAtom, got: {json_value}"
            )
        key = next(iter(json_value))
        type = ClaimAtomType.from_json_dict(key)
        if key == "v0":
            v0 = ClaimOfferAtomV0.from_json_dict(json_value["v0"])
            return cls(type=type, v0=v0)
        if key == "order_book":
            order_book = ClaimOfferAtom.from_json_dict(json_value["order_book"])
            return cls(type=type, order_book=order_book)
        if key == "liquidity_pool":
            liquidity_pool = ClaimLiquidityAtom.from_json_dict(
                json_value["liquidity_pool"]
            )
            return cls(type=type, liquidity_pool=liquidity_pool)
        raise ValueError(f"Unknown key '{key}' for ClaimAtom")

    def __hash__(self):
        return hash(
            (
                self.type,
                self.v0,
                self.order_book,
                self.liquidity_pool,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.v0 == other.v0
            and self.order_book == other.order_book
            and self.liquidity_pool == other.liquidity_pool
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        if self.v0 is not None:
            out.append(f"v0={self.v0}")
        if self.order_book is not None:
            out.append(f"order_book={self.order_book}")
        if self.liquidity_pool is not None:
            out.append(f"liquidity_pool={self.liquidity_pool}")
        return f"<ClaimAtom [{', '.join(out)}]>"
