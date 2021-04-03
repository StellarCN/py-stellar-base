# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .account_id import AccountID
from .asset import Asset
from .int64 import Int64

__all__ = ["ClaimOfferAtom"]


class ClaimOfferAtom:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct ClaimOfferAtom
    {
        // emitted to identify the offer
        AccountID sellerID; // Account that owns the offer
        int64 offerID;

        // amount and asset taken from the owner
        Asset assetSold;
        int64 amountSold;

        // amount and asset sent to the owner
        Asset assetBought;
        int64 amountBought;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        seller_id: AccountID,
        offer_id: Int64,
        asset_sold: Asset,
        amount_sold: Int64,
        asset_bought: Asset,
        amount_bought: Int64,
    ) -> None:
        self.seller_id = seller_id
        self.offer_id = offer_id
        self.asset_sold = asset_sold
        self.amount_sold = amount_sold
        self.asset_bought = asset_bought
        self.amount_bought = amount_bought

    def pack(self, packer: Packer) -> None:
        self.seller_id.pack(packer)
        self.offer_id.pack(packer)
        self.asset_sold.pack(packer)
        self.amount_sold.pack(packer)
        self.asset_bought.pack(packer)
        self.amount_bought.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ClaimOfferAtom":
        seller_id = AccountID.unpack(unpacker)
        offer_id = Int64.unpack(unpacker)
        asset_sold = Asset.unpack(unpacker)
        amount_sold = Int64.unpack(unpacker)
        asset_bought = Asset.unpack(unpacker)
        amount_bought = Int64.unpack(unpacker)
        return cls(
            seller_id=seller_id,
            offer_id=offer_id,
            asset_sold=asset_sold,
            amount_sold=amount_sold,
            asset_bought=asset_bought,
            amount_bought=amount_bought,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "ClaimOfferAtom":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ClaimOfferAtom":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.seller_id == other.seller_id
            and self.offer_id == other.offer_id
            and self.asset_sold == other.asset_sold
            and self.amount_sold == other.amount_sold
            and self.asset_bought == other.asset_bought
            and self.amount_bought == other.amount_bought
        )

    def __str__(self):
        out = [
            f"seller_id={self.seller_id}",
            f"offer_id={self.offer_id}",
            f"asset_sold={self.asset_sold}",
            f"amount_sold={self.amount_sold}",
            f"asset_bought={self.asset_bought}",
            f"amount_bought={self.amount_bought}",
        ]
        return f"<ClaimOfferAtom {[', '.join(out)]}>"
