# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List, Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .claim_predicate_type import ClaimPredicateType
from .int64 import Int64

__all__ = ["ClaimPredicate"]


class ClaimPredicate:
    """
    XDR Source Code::

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
    """

    def __init__(
        self,
        type: ClaimPredicateType,
        and_predicates: Optional[List["ClaimPredicate"]] = None,
        or_predicates: Optional[List["ClaimPredicate"]] = None,
        not_predicate: Optional[Optional["ClaimPredicate"]] = None,
        abs_before: Optional[Int64] = None,
        rel_before: Optional[Int64] = None,
    ) -> None:
        _expect_max_length = 2
        if and_predicates and len(and_predicates) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `and_predicates` should be {_expect_max_length}, but got {len(and_predicates)}."
            )
        _expect_max_length = 2
        if or_predicates and len(or_predicates) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `or_predicates` should be {_expect_max_length}, but got {len(or_predicates)}."
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
            for and_predicates_item in self.and_predicates:
                and_predicates_item.pack(packer)
            return
        if self.type == ClaimPredicateType.CLAIM_PREDICATE_OR:
            if self.or_predicates is None:
                raise ValueError("or_predicates should not be None.")
            packer.pack_uint(len(self.or_predicates))
            for or_predicates_item in self.or_predicates:
                or_predicates_item.pack(packer)
            return
        if self.type == ClaimPredicateType.CLAIM_PREDICATE_NOT:
            if self.not_predicate is None:
                packer.pack_uint(0)
            else:
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
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ClaimPredicate:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = ClaimPredicateType.unpack(unpacker)
        if type == ClaimPredicateType.CLAIM_PREDICATE_UNCONDITIONAL:
            return cls(type=type)
        if type == ClaimPredicateType.CLAIM_PREDICATE_AND:
            length = unpacker.unpack_uint()
            _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
            if _remaining < length:
                raise ValueError(
                    f"and_predicates length {length} exceeds remaining input length {_remaining}"
                )
            and_predicates = []
            for _ in range(length):
                and_predicates.append(ClaimPredicate.unpack(unpacker, depth_limit - 1))
            return cls(type=type, and_predicates=and_predicates)
        if type == ClaimPredicateType.CLAIM_PREDICATE_OR:
            length = unpacker.unpack_uint()
            _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
            if _remaining < length:
                raise ValueError(
                    f"or_predicates length {length} exceeds remaining input length {_remaining}"
                )
            or_predicates = []
            for _ in range(length):
                or_predicates.append(ClaimPredicate.unpack(unpacker, depth_limit - 1))
            return cls(type=type, or_predicates=or_predicates)
        if type == ClaimPredicateType.CLAIM_PREDICATE_NOT:
            not_predicate = (
                ClaimPredicate.unpack(unpacker, depth_limit - 1)
                if unpacker.unpack_uint()
                else None
            )
            return cls(type=type, not_predicate=not_predicate)
        if type == ClaimPredicateType.CLAIM_PREDICATE_BEFORE_ABSOLUTE_TIME:
            abs_before = Int64.unpack(unpacker, depth_limit - 1)
            return cls(type=type, abs_before=abs_before)
        if type == ClaimPredicateType.CLAIM_PREDICATE_BEFORE_RELATIVE_TIME:
            rel_before = Int64.unpack(unpacker, depth_limit - 1)
            return cls(type=type, rel_before=rel_before)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ClaimPredicate:
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
    def from_xdr(cls, xdr: str) -> ClaimPredicate:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ClaimPredicate:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.type == ClaimPredicateType.CLAIM_PREDICATE_UNCONDITIONAL:
            return "unconditional"
        if self.type == ClaimPredicateType.CLAIM_PREDICATE_AND:
            assert self.and_predicates is not None
            return {"and": [item.to_json_dict() for item in self.and_predicates]}
        if self.type == ClaimPredicateType.CLAIM_PREDICATE_OR:
            assert self.or_predicates is not None
            return {"or": [item.to_json_dict() for item in self.or_predicates]}
        if self.type == ClaimPredicateType.CLAIM_PREDICATE_NOT:
            assert self.not_predicate is not None
            return {"not": self.not_predicate.to_json_dict()}
        if self.type == ClaimPredicateType.CLAIM_PREDICATE_BEFORE_ABSOLUTE_TIME:
            assert self.abs_before is not None
            return {"before_absolute_time": self.abs_before.to_json_dict()}
        if self.type == ClaimPredicateType.CLAIM_PREDICATE_BEFORE_RELATIVE_TIME:
            assert self.rel_before is not None
            return {"before_relative_time": self.rel_before.to_json_dict()}
        raise ValueError(f"Unknown type in ClaimPredicate: {self.type}")

    @classmethod
    def from_json_dict(cls, json_value: str | dict) -> ClaimPredicate:
        if isinstance(json_value, str):
            if json_value not in ("unconditional",):
                raise ValueError(
                    f"Unexpected string '{json_value}' for ClaimPredicate, must be one of: unconditional"
                )
            type = ClaimPredicateType.from_json_dict(json_value)
            return cls(type=type)
        if not isinstance(json_value, dict) or len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for ClaimPredicate, got: {json_value}"
            )
        key = next(iter(json_value))
        type = ClaimPredicateType.from_json_dict(key)
        if key == "and":
            and_predicates = [
                ClaimPredicate.from_json_dict(item) for item in json_value["and"]
            ]
            return cls(type=type, and_predicates=and_predicates)
        if key == "or":
            or_predicates = [
                ClaimPredicate.from_json_dict(item) for item in json_value["or"]
            ]
            return cls(type=type, or_predicates=or_predicates)
        if key == "not":
            not_predicate = ClaimPredicate.from_json_dict(json_value["not"])
            return cls(type=type, not_predicate=not_predicate)
        if key == "before_absolute_time":
            abs_before = Int64.from_json_dict(json_value["before_absolute_time"])
            return cls(type=type, abs_before=abs_before)
        if key == "before_relative_time":
            rel_before = Int64.from_json_dict(json_value["before_relative_time"])
            return cls(type=type, rel_before=rel_before)
        raise ValueError(f"Unknown key '{key}' for ClaimPredicate")

    def __hash__(self):
        return hash(
            (
                self.type,
                self.and_predicates,
                self.or_predicates,
                self.not_predicate,
                self.abs_before,
                self.rel_before,
            )
        )

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

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        if self.and_predicates is not None:
            out.append(f"and_predicates={self.and_predicates}")
        if self.or_predicates is not None:
            out.append(f"or_predicates={self.or_predicates}")
        if self.not_predicate is not None:
            out.append(f"not_predicate={self.not_predicate}")
        if self.abs_before is not None:
            out.append(f"abs_before={self.abs_before}")
        if self.rel_before is not None:
            out.append(f"rel_before={self.rel_before}")
        return f"<ClaimPredicate [{', '.join(out)}]>"
