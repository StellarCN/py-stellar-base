# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .claimant_type import ClaimantType
from .claimant_v0 import ClaimantV0

__all__ = ["Claimant"]


class Claimant:
    """
    XDR Source Code::

        union Claimant switch (ClaimantType type)
        {
        case CLAIMANT_TYPE_V0:
            struct
            {
                AccountID destination;    // The account that can use this condition
                ClaimPredicate predicate; // Claimable if predicate is true
            } v0;
        };
    """

    def __init__(
        self,
        type: ClaimantType,
        v0: Optional[ClaimantV0] = None,
    ) -> None:
        self.type = type
        self.v0 = v0

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == ClaimantType.CLAIMANT_TYPE_V0:
            if self.v0 is None:
                raise ValueError("v0 should not be None.")
            self.v0.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> Claimant:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = ClaimantType.unpack(unpacker)
        if type == ClaimantType.CLAIMANT_TYPE_V0:
            v0 = ClaimantV0.unpack(unpacker, depth_limit - 1)
            return cls(type=type, v0=v0)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Claimant:
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
    def from_xdr(cls, xdr: str) -> Claimant:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Claimant:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.type == ClaimantType.CLAIMANT_TYPE_V0:
            assert self.v0 is not None
            return {"claimant_type_v0": self.v0.to_json_dict()}
        raise ValueError(f"Unknown type in Claimant: {self.type}")

    @classmethod
    def from_json_dict(cls, json_value: dict) -> Claimant:
        if len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for Claimant, got: {json_value}"
            )
        key = next(iter(json_value))
        type = ClaimantType.from_json_dict(key)
        if key == "claimant_type_v0":
            v0 = ClaimantV0.from_json_dict(json_value["claimant_type_v0"])
            return cls(type=type, v0=v0)
        raise ValueError(f"Unknown key '{key}' for Claimant")

    def __hash__(self):
        return hash(
            (
                self.type,
                self.v0,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.type == other.type and self.v0 == other.v0

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        if self.v0 is not None:
            out.append(f"v0={self.v0}")
        return f"<Claimant [{', '.join(out)}]>"
