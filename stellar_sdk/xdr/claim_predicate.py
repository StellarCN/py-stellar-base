# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List, Optional
from xdrlib import Packer, Unpacker

from ..exceptions import ValueError
from .claim_predicate_type import ClaimPredicateType
from .int64 import Int64

__all__ = ["ClaimPredicate"]


class ClaimPredicate:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union ClaimPredicate switch (ClaimPredicateType type)
    {
    case CLAIM_PREDICATE_UNCONDITIONAL:
        void;
    case CLAIM_PREDICATE_AND:
        ClaimPredicate andPredicates<2>;
    case CLAIM_PREDICATE_OR:
        ClaimPredicate orPredicates<2>;
    case CLAIM_PREDICATE_NOT:
        ClaimPredicate* notPredicate;
    case CLAIM_PREDICATE_BEFORE_ABSOLUTE_TIME:
        int64 absBefore; // Predicate will be true if closeTime < absBefore
    case CLAIM_PREDICATE_BEFORE_RELATIVE_TIME:
        int64 relBefore; // Seconds since closeTime of the ledger in which the
                         // ClaimableBalanceEntry was created
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: ClaimPredicateType,
        and_predicates: List["ClaimPredicate"] = None,
        or_predicates: List["ClaimPredicate"] = None,
        not_predicate: Optional["ClaimPredicate"] = None,
        abs_before: Int64 = None,
        rel_before: Int64 = None,
    ) -> None:
        if and_predicates and len(and_predicates) > 2:
            raise ValueError(
                f"The maximum length of `and_predicates` should be 2, but got {len(and_predicates)}."
            )
        if or_predicates and len(or_predicates) > 2:
            raise ValueError(
                f"The maximum length of `or_predicates` should be 2, but got {len(or_predicates)}."
            )
        self.type = type
        self.and_predicates = and_predicates
        self.or_predicates = or_predicates
        self.not_predicate = not_predicate
        self.abs_before = abs_before
        self.rel_before = rel_before

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == ClaimPredicateType.CLAIM_PREDICATE_UNCONDITIONAL:
            return
        if self.type == ClaimPredicateType.CLAIM_PREDICATE_AND:
            if self.and_predicates is None:
                raise ValueError("and_predicates should not be None.")
            packer.pack_uint(len(self.and_predicates))
            for and_predicate in self.and_predicates:
                and_predicate.pack(packer)
            return
        if self.type == ClaimPredicateType.CLAIM_PREDICATE_OR:
            if self.or_predicates is None:
                raise ValueError("or_predicates should not be None.")
            packer.pack_uint(len(self.or_predicates))
            for or_predicate in self.or_predicates:
                or_predicate.pack(packer)
            return
        if self.type == ClaimPredicateType.CLAIM_PREDICATE_NOT:
            if self.not_predicate is None:
                packer.pack_uint(0)
                return
            packer.pack_uint(1)
            if self.not_predicate is None:
                raise ValueError("not_predicate should not be None.")
            self.not_predicate.pack(packer)
            return
        if self.type == ClaimPredicateType.CLAIM_PREDICATE_BEFORE_ABSOLUTE_TIME:
            if self.abs_before is None:
                raise ValueError("abs_before should not be None.")
            self.abs_before.pack(packer)
            return
        if self.type == ClaimPredicateType.CLAIM_PREDICATE_BEFORE_RELATIVE_TIME:
            if self.rel_before is None:
                raise ValueError("rel_before should not be None.")
            self.rel_before.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ClaimPredicate":
        type = ClaimPredicateType.unpack(unpacker)
        if type == ClaimPredicateType.CLAIM_PREDICATE_UNCONDITIONAL:
            return cls(type)
        if type == ClaimPredicateType.CLAIM_PREDICATE_AND:
            length = unpacker.unpack_uint()
            and_predicates = []
            for _ in range(length):
                and_predicates.append(ClaimPredicate.unpack(unpacker))
            return cls(type, and_predicates=and_predicates)
        if type == ClaimPredicateType.CLAIM_PREDICATE_OR:
            length = unpacker.unpack_uint()
            or_predicates = []
            for _ in range(length):
                or_predicates.append(ClaimPredicate.unpack(unpacker))
            return cls(type, or_predicates=or_predicates)
        if type == ClaimPredicateType.CLAIM_PREDICATE_NOT:
            not_predicate = (
                ClaimPredicate.unpack(unpacker) if unpacker.unpack_uint() else None
            )
            if not_predicate is None:
                raise ValueError("not_predicate should not be None.")
            return cls(type, not_predicate=not_predicate)
        if type == ClaimPredicateType.CLAIM_PREDICATE_BEFORE_ABSOLUTE_TIME:
            abs_before = Int64.unpack(unpacker)
            if abs_before is None:
                raise ValueError("abs_before should not be None.")
            return cls(type, abs_before=abs_before)
        if type == ClaimPredicateType.CLAIM_PREDICATE_BEFORE_RELATIVE_TIME:
            rel_before = Int64.unpack(unpacker)
            if rel_before is None:
                raise ValueError("rel_before should not be None.")
            return cls(type, rel_before=rel_before)
        return cls(type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "ClaimPredicate":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ClaimPredicate":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.and_predicates == other.and_predicates
            and self.or_predicates == other.or_predicates
            and self.not_predicate == other.not_predicate
            and self.abs_before == other.abs_before
            and self.rel_before == other.rel_before
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(
            f"and_predicates={self.and_predicates}"
        ) if self.and_predicates is not None else None
        out.append(
            f"or_predicates={self.or_predicates}"
        ) if self.or_predicates is not None else None
        out.append(
            f"not_predicate={self.not_predicate}"
        ) if self.not_predicate is not None else None
        out.append(
            f"abs_before={self.abs_before}"
        ) if self.abs_before is not None else None
        out.append(
            f"rel_before={self.rel_before}"
        ) if self.rel_before is not None else None
        return f"<ClaimPredicate {[', '.join(out)]}>"
