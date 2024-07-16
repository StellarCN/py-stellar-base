# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

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
        v0: ClaimOfferAtomV0 = None,
        order_book: ClaimOfferAtom = None,
        liquidity_pool: ClaimLiquidityAtom = None,
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

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ClaimAtom:
        type = ClaimAtomType.unpack(unpacker)
        if type == ClaimAtomType.CLAIM_ATOM_TYPE_V0:
            v0 = ClaimOfferAtomV0.unpack(unpacker)
            return cls(type=type, v0=v0)
        if type == ClaimAtomType.CLAIM_ATOM_TYPE_ORDER_BOOK:
            order_book = ClaimOfferAtom.unpack(unpacker)
            return cls(type=type, order_book=order_book)
        if type == ClaimAtomType.CLAIM_ATOM_TYPE_LIQUIDITY_POOL:
            liquidity_pool = ClaimLiquidityAtom.unpack(unpacker)
            return cls(type=type, liquidity_pool=liquidity_pool)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ClaimAtom:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ClaimAtom:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
        out.append(f"v0={self.v0}") if self.v0 is not None else None
        (
            out.append(f"order_book={self.order_book}")
            if self.order_book is not None
            else None
        )
        (
            out.append(f"liquidity_pool={self.liquidity_pool}")
            if self.liquidity_pool is not None
            else None
        )
        return f"<ClaimAtom [{', '.join(out)}]>"
