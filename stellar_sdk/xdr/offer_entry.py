# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .account_id import AccountID
from .asset import Asset
from .base import DEFAULT_XDR_MAX_DEPTH
from .int64 import Int64
from .offer_entry_ext import OfferEntryExt
from .price import Price
from .uint32 import Uint32

__all__ = ["OfferEntry"]


class OfferEntry:
    """
    XDR Source Code::

        struct OfferEntry
        {
            AccountID sellerID;
            int64 offerID;
            Asset selling; // A
            Asset buying;  // B
            int64 amount;  // amount of A

            /* price for this offer:
                price of A in terms of B
                price=AmountB/AmountA=priceNumerator/priceDenominator
                price is after fees
            */
            Price price;
            uint32 flags; // see OfferEntryFlags

            // reserved for future use
            union switch (int v)
            {
            case 0:
                void;
            }
            ext;
        };
    """

    def __init__(
        self,
        seller_id: AccountID,
        offer_id: Int64,
        selling: Asset,
        buying: Asset,
        amount: Int64,
        price: Price,
        flags: Uint32,
        ext: OfferEntryExt,
    ) -> None:
        self.seller_id = seller_id
        self.offer_id = offer_id
        self.selling = selling
        self.buying = buying
        self.amount = amount
        self.price = price
        self.flags = flags
        self.ext = ext

    def pack(self, packer: Packer) -> None:
        self.seller_id.pack(packer)
        self.offer_id.pack(packer)
        self.selling.pack(packer)
        self.buying.pack(packer)
        self.amount.pack(packer)
        self.price.pack(packer)
        self.flags.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> OfferEntry:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        seller_id = AccountID.unpack(unpacker, depth_limit - 1)
        offer_id = Int64.unpack(unpacker, depth_limit - 1)
        selling = Asset.unpack(unpacker, depth_limit - 1)
        buying = Asset.unpack(unpacker, depth_limit - 1)
        amount = Int64.unpack(unpacker, depth_limit - 1)
        price = Price.unpack(unpacker, depth_limit - 1)
        flags = Uint32.unpack(unpacker, depth_limit - 1)
        ext = OfferEntryExt.unpack(unpacker, depth_limit - 1)
        return cls(
            seller_id=seller_id,
            offer_id=offer_id,
            selling=selling,
            buying=buying,
            amount=amount,
            price=price,
            flags=flags,
            ext=ext,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> OfferEntry:
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
    def from_xdr(cls, xdr: str) -> OfferEntry:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> OfferEntry:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "seller_id": self.seller_id.to_json_dict(),
            "offer_id": self.offer_id.to_json_dict(),
            "selling": self.selling.to_json_dict(),
            "buying": self.buying.to_json_dict(),
            "amount": self.amount.to_json_dict(),
            "price": self.price.to_json_dict(),
            "flags": self.flags.to_json_dict(),
            "ext": self.ext.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> OfferEntry:
        seller_id = AccountID.from_json_dict(json_dict["seller_id"])
        offer_id = Int64.from_json_dict(json_dict["offer_id"])
        selling = Asset.from_json_dict(json_dict["selling"])
        buying = Asset.from_json_dict(json_dict["buying"])
        amount = Int64.from_json_dict(json_dict["amount"])
        price = Price.from_json_dict(json_dict["price"])
        flags = Uint32.from_json_dict(json_dict["flags"])
        ext = OfferEntryExt.from_json_dict(json_dict["ext"])
        return cls(
            seller_id=seller_id,
            offer_id=offer_id,
            selling=selling,
            buying=buying,
            amount=amount,
            price=price,
            flags=flags,
            ext=ext,
        )

    def __hash__(self):
        return hash(
            (
                self.seller_id,
                self.offer_id,
                self.selling,
                self.buying,
                self.amount,
                self.price,
                self.flags,
                self.ext,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.seller_id == other.seller_id
            and self.offer_id == other.offer_id
            and self.selling == other.selling
            and self.buying == other.buying
            and self.amount == other.amount
            and self.price == other.price
            and self.flags == other.flags
            and self.ext == other.ext
        )

    def __repr__(self):
        out = [
            f"seller_id={self.seller_id}",
            f"offer_id={self.offer_id}",
            f"selling={self.selling}",
            f"buying={self.buying}",
            f"amount={self.amount}",
            f"price={self.price}",
            f"flags={self.flags}",
            f"ext={self.ext}",
        ]
        return f"<OfferEntry [{', '.join(out)}]>"
