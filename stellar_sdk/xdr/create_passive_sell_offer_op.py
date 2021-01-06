# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .asset import Asset
from .int64 import Int64
from .price import Price

__all__ = ["CreatePassiveSellOfferOp"]


class CreatePassiveSellOfferOp:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct CreatePassiveSellOfferOp
    {
        Asset selling; // A
        Asset buying;  // B
        int64 amount;  // amount taker gets. if set to 0, delete the offer
        Price price;   // cost of A in terms of B
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self, selling: Asset, buying: Asset, amount: Int64, price: Price,
    ) -> None:
        self.selling = selling
        self.buying = buying
        self.amount = amount
        self.price = price

    def pack(self, packer: Packer) -> None:
        self.selling.pack(packer)
        self.buying.pack(packer)
        self.amount.pack(packer)
        self.price.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "CreatePassiveSellOfferOp":
        selling = Asset.unpack(unpacker)
        buying = Asset.unpack(unpacker)
        amount = Int64.unpack(unpacker)
        price = Price.unpack(unpacker)
        return cls(selling=selling, buying=buying, amount=amount, price=price,)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "CreatePassiveSellOfferOp":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "CreatePassiveSellOfferOp":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.selling == other.selling
            and self.buying == other.buying
            and self.amount == other.amount
            and self.price == other.price
        )

    def __str__(self):
        out = [
            f"selling={self.selling}",
            f"buying={self.buying}",
            f"amount={self.amount}",
            f"price={self.price}",
        ]
        return f"<CreatePassiveSellOfferOp {[', '.join(out)]}>"
