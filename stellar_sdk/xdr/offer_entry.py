# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .account_id import AccountID
from .asset import Asset
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
    def unpack(cls, unpacker: Unpacker) -> OfferEntry:
        seller_id = AccountID.unpack(unpacker)
        offer_id = Int64.unpack(unpacker)
        selling = Asset.unpack(unpacker)
        buying = Asset.unpack(unpacker)
        amount = Int64.unpack(unpacker)
        price = Price.unpack(unpacker)
        flags = Uint32.unpack(unpacker)
        ext = OfferEntryExt.unpack(unpacker)
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
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> OfferEntry:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
