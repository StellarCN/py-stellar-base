# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .account_id import AccountID
from .base import DEFAULT_XDR_MAX_DEPTH
from .claim_predicate import ClaimPredicate

__all__ = ["ClaimantV0"]


class ClaimantV0:
    """
    XDR Source Code::

        struct
            {
                AccountID destination;    // The account that can use this condition
                ClaimPredicate predicate; // Claimable if predicate is true
            }
    """

    def __init__(
        self,
        destination: AccountID,
        predicate: ClaimPredicate,
    ) -> None:
        self.destination = destination
        self.predicate = predicate

    def pack(self, packer: Packer) -> None:
        self.destination.pack(packer)
        self.predicate.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ClaimantV0:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        destination = AccountID.unpack(unpacker, depth_limit - 1)
        predicate = ClaimPredicate.unpack(unpacker, depth_limit - 1)
        return cls(
            destination=destination,
            predicate=predicate,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ClaimantV0:
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
    def from_xdr(cls, xdr: str) -> ClaimantV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ClaimantV0:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "destination": self.destination.to_json_dict(),
            "predicate": self.predicate.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> ClaimantV0:
        destination = AccountID.from_json_dict(json_dict["destination"])
        predicate = ClaimPredicate.from_json_dict(json_dict["predicate"])
        return cls(
            destination=destination,
            predicate=predicate,
        )

    def __hash__(self):
        return hash(
            (
                self.destination,
                self.predicate,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.destination == other.destination and self.predicate == other.predicate
        )

    def __repr__(self):
        out = [
            f"destination={self.destination}",
            f"predicate={self.predicate}",
        ]
        return f"<ClaimantV0 [{', '.join(out)}]>"
