# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

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
        v0: ClaimantV0 = None,
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

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> Claimant:
        type = ClaimantType.unpack(unpacker)
        if type == ClaimantType.CLAIMANT_TYPE_V0:
            v0 = ClaimantV0.unpack(unpacker)
            return cls(type=type, v0=v0)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Claimant:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> Claimant:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
        out.append(f"v0={self.v0}") if self.v0 is not None else None
        return f"<Claimant [{', '.join(out)}]>"
