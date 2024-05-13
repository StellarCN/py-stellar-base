# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .asset import Asset
from .int64 import Int64
from .uint256 import Uint256

__all__ = ["ClaimOfferAtomV0"]


class ClaimOfferAtomV0:
    """
    XDR Source Code::

        struct ClaimOfferAtomV0
        {
            // emitted to identify the offer
            uint256 sellerEd25519; // Account that owns the offer
            int64 offerID;

            // amount and asset taken from the owner
            Asset assetSold;
            int64 amountSold;

            // amount and asset sent to the owner
            Asset assetBought;
            int64 amountBought;
        };
    """

    def __init__(
        self,
        seller_ed25519: Uint256,
        offer_id: Int64,
        asset_sold: Asset,
        amount_sold: Int64,
        asset_bought: Asset,
        amount_bought: Int64,
    ) -> None:
        self.seller_ed25519 = seller_ed25519
        self.offer_id = offer_id
        self.asset_sold = asset_sold
        self.amount_sold = amount_sold
        self.asset_bought = asset_bought
        self.amount_bought = amount_bought

    def pack(self, packer: Packer) -> None:
        self.seller_ed25519.pack(packer)
        self.offer_id.pack(packer)
        self.asset_sold.pack(packer)
        self.amount_sold.pack(packer)
        self.asset_bought.pack(packer)
        self.amount_bought.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ClaimOfferAtomV0:
        seller_ed25519 = Uint256.unpack(unpacker)
        offer_id = Int64.unpack(unpacker)
        asset_sold = Asset.unpack(unpacker)
        amount_sold = Int64.unpack(unpacker)
        asset_bought = Asset.unpack(unpacker)
        amount_bought = Int64.unpack(unpacker)
        return cls(
            seller_ed25519=seller_ed25519,
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
    def from_xdr_bytes(cls, xdr: bytes) -> ClaimOfferAtomV0:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ClaimOfferAtomV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.seller_ed25519,
                self.offer_id,
                self.asset_sold,
                self.amount_sold,
                self.asset_bought,
                self.amount_bought,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.seller_ed25519 == other.seller_ed25519
            and self.offer_id == other.offer_id
            and self.asset_sold == other.asset_sold
            and self.amount_sold == other.amount_sold
            and self.asset_bought == other.asset_bought
            and self.amount_bought == other.amount_bought
        )

    def __repr__(self):
        out = [
            f"seller_ed25519={self.seller_ed25519}",
            f"offer_id={self.offer_id}",
            f"asset_sold={self.asset_sold}",
            f"amount_sold={self.amount_sold}",
            f"asset_bought={self.asset_bought}",
            f"amount_bought={self.amount_bought}",
        ]
        return f"<ClaimOfferAtomV0 [{', '.join(out)}]>"
