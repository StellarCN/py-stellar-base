# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .asset import Asset
from .int64 import Int64
from .price import Price

__all__ = ["ManageBuyOfferOp"]


class ManageBuyOfferOp:
    """
    XDR Source Code
    ----------------------------------------------------------------
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
    ----------------------------------------------------------------
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
    def unpack(cls, unpacker: Unpacker) -> "ManageBuyOfferOp":
        selling = Asset.unpack(unpacker)
        buying = Asset.unpack(unpacker)
        buy_amount = Int64.unpack(unpacker)
        price = Price.unpack(unpacker)
        offer_id = Int64.unpack(unpacker)
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
    def from_xdr_bytes(cls, xdr: bytes) -> "ManageBuyOfferOp":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ManageBuyOfferOp":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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

    def __str__(self):
        out = [
            f"selling={self.selling}",
            f"buying={self.buying}",
            f"buy_amount={self.buy_amount}",
            f"price={self.price}",
            f"offer_id={self.offer_id}",
        ]
        return f"<ManageBuyOfferOp {[', '.join(out)]}>"
