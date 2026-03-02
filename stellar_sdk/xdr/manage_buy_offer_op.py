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

__all__ = ["ManageBuyOfferOp"]


class ManageBuyOfferOp:
    """
    XDR Source Code::

        struct ManageBuyOfferOp
        {
            Asset selling;
            Asset buying;
            int64 buyAmount; // amount being bought. if set to 0, delete the offer
            Price price;     // price of thing being bought in terms of what you are
                             // selling

            // 0=create a new offer, otherwise edit an existing offer
            int64 offerID;
        };
    """

    def __init__(
        self,
        selling: Asset,
        buying: Asset,
        buy_amount: Int64,
        price: Price,
        offer_id: Int64,
    ) -> None:
        self.selling = selling
        self.buying = buying
        self.buy_amount = buy_amount
        self.price = price
        self.offer_id = offer_id

    def pack(self, packer: Packer) -> None:
        self.selling.pack(packer)
        self.buying.pack(packer)
        self.buy_amount.pack(packer)
        self.price.pack(packer)
        self.offer_id.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ManageBuyOfferOp:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        selling = Asset.unpack(unpacker, depth_limit - 1)
        buying = Asset.unpack(unpacker, depth_limit - 1)
        buy_amount = Int64.unpack(unpacker, depth_limit - 1)
        price = Price.unpack(unpacker, depth_limit - 1)
        offer_id = Int64.unpack(unpacker, depth_limit - 1)
        return cls(
            selling=selling,
            buying=buying,
            buy_amount=buy_amount,
            price=price,
            offer_id=offer_id,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ManageBuyOfferOp:
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
    def from_xdr(cls, xdr: str) -> ManageBuyOfferOp:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ManageBuyOfferOp:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "selling": self.selling.to_json_dict(),
            "buying": self.buying.to_json_dict(),
            "buy_amount": self.buy_amount.to_json_dict(),
            "price": self.price.to_json_dict(),
            "offer_id": self.offer_id.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> ManageBuyOfferOp:
        selling = Asset.from_json_dict(json_dict["selling"])
        buying = Asset.from_json_dict(json_dict["buying"])
        buy_amount = Int64.from_json_dict(json_dict["buy_amount"])
        price = Price.from_json_dict(json_dict["price"])
        offer_id = Int64.from_json_dict(json_dict["offer_id"])
        return cls(
            selling=selling,
            buying=buying,
            buy_amount=buy_amount,
            price=price,
            offer_id=offer_id,
        )

    def __hash__(self):
        return hash(
            (
                self.selling,
                self.buying,
                self.buy_amount,
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
            and self.buy_amount == other.buy_amount
            and self.price == other.price
            and self.offer_id == other.offer_id
        )

    def __repr__(self):
        out = [
            f"selling={self.selling}",
            f"buying={self.buying}",
            f"buy_amount={self.buy_amount}",
            f"price={self.price}",
            f"offer_id={self.offer_id}",
        ]
        return f"<ManageBuyOfferOp [{', '.join(out)}]>"
