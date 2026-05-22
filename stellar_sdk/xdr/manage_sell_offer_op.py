# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .asset import Asset
from .base import DEFAULT_XDR_MAX_DEPTH
from .int64 import Int64
from .price import Price

__all__ = ["ManageSellOfferOp"]


class ManageSellOfferOp:
    """
    XDR Source Code::

        struct ManageSellOfferOp
        {
            Asset selling;
            Asset buying;
            int64 amount; // amount being sold. if set to 0, delete the offer
            Price price;  // price of thing being sold in terms of what you are buying

            // 0=create a new offer, otherwise edit an existing offer
            int64 offerID;
        };
    """

    def __init__(
        self,
        selling: Asset,
        buying: Asset,
        amount: Int64,
        price: Price,
        offer_id: Int64,
    ) -> None:
        self.selling = selling
        self.buying = buying
        self.amount = amount
        self.price = price
        self.offer_id = offer_id

    def pack(self, packer: Packer) -> None:
        self.selling.pack(packer)
        self.buying.pack(packer)
        self.amount.pack(packer)
        self.price.pack(packer)
        self.offer_id.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ManageSellOfferOp:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        selling = Asset.unpack(unpacker, depth_limit - 1)
        buying = Asset.unpack(unpacker, depth_limit - 1)
        amount = Int64.unpack(unpacker, depth_limit - 1)
        price = Price.unpack(unpacker, depth_limit - 1)
        offer_id = Int64.unpack(unpacker, depth_limit - 1)
        return cls(
            selling=selling,
            buying=buying,
            amount=amount,
            price=price,
            offer_id=offer_id,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ManageSellOfferOp:
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
    def from_xdr(cls, xdr: str) -> ManageSellOfferOp:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ManageSellOfferOp:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "selling": self.selling.to_json_dict(),
            "buying": self.buying.to_json_dict(),
            "amount": self.amount.to_json_dict(),
            "price": self.price.to_json_dict(),
            "offer_id": self.offer_id.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> ManageSellOfferOp:
        selling = Asset.from_json_dict(json_dict["selling"])
        buying = Asset.from_json_dict(json_dict["buying"])
        amount = Int64.from_json_dict(json_dict["amount"])
        price = Price.from_json_dict(json_dict["price"])
        offer_id = Int64.from_json_dict(json_dict["offer_id"])
        return cls(
            selling=selling,
            buying=buying,
            amount=amount,
            price=price,
            offer_id=offer_id,
        )

    def __hash__(self):
        return hash(
            (
                self.selling,
                self.buying,
                self.amount,
                self.price,
                self.offer_id,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.selling == other.selling
            and self.buying == other.buying
            and self.amount == other.amount
            and self.price == other.price
            and self.offer_id == other.offer_id
        )

    def __repr__(self):
        out = [
            f"selling={self.selling}",
            f"buying={self.buying}",
            f"amount={self.amount}",
            f"price={self.price}",
            f"offer_id={self.offer_id}",
        ]
        return f"<ManageSellOfferOp [{', '.join(out)}]>"
