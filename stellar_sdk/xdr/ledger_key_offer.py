# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .account_id import AccountID
from .base import DEFAULT_XDR_MAX_DEPTH
from .int64 import Int64

__all__ = ["LedgerKeyOffer"]


class LedgerKeyOffer:
    """
    XDR Source Code::

        struct
            {
                AccountID sellerID;
                int64 offerID;
            }
    """

    def __init__(
        self,
        seller_id: AccountID,
        offer_id: Int64,
    ) -> None:
        self.seller_id = seller_id
        self.offer_id = offer_id

    def pack(self, packer: Packer) -> None:
        self.seller_id.pack(packer)
        self.offer_id.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> LedgerKeyOffer:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        seller_id = AccountID.unpack(unpacker, depth_limit - 1)
        offer_id = Int64.unpack(unpacker, depth_limit - 1)
        return cls(
            seller_id=seller_id,
            offer_id=offer_id,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerKeyOffer:
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
    def from_xdr(cls, xdr: str) -> LedgerKeyOffer:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LedgerKeyOffer:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "seller_id": self.seller_id.to_json_dict(),
            "offer_id": self.offer_id.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> LedgerKeyOffer:
        seller_id = AccountID.from_json_dict(json_dict["seller_id"])
        offer_id = Int64.from_json_dict(json_dict["offer_id"])
        return cls(
            seller_id=seller_id,
            offer_id=offer_id,
        )

    def __hash__(self):
        return hash(
            (
                self.seller_id,
                self.offer_id,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.seller_id == other.seller_id and self.offer_id == other.offer_id

    def __repr__(self):
        out = [
            f"seller_id={self.seller_id}",
            f"offer_id={self.offer_id}",
        ]
        return f"<LedgerKeyOffer [{', '.join(out)}]>"
