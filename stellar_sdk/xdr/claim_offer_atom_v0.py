# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .asset import Asset
from .base import DEFAULT_XDR_MAX_DEPTH
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ClaimOfferAtomV0:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        seller_ed25519 = Uint256.unpack(unpacker, depth_limit - 1)
        offer_id = Int64.unpack(unpacker, depth_limit - 1)
        asset_sold = Asset.unpack(unpacker, depth_limit - 1)
        amount_sold = Int64.unpack(unpacker, depth_limit - 1)
        asset_bought = Asset.unpack(unpacker, depth_limit - 1)
        amount_bought = Int64.unpack(unpacker, depth_limit - 1)
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ClaimOfferAtomV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ClaimOfferAtomV0:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "seller_ed25519": self.seller_ed25519.to_json_dict(),
            "offer_id": self.offer_id.to_json_dict(),
            "asset_sold": self.asset_sold.to_json_dict(),
            "amount_sold": self.amount_sold.to_json_dict(),
            "asset_bought": self.asset_bought.to_json_dict(),
            "amount_bought": self.amount_bought.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> ClaimOfferAtomV0:
        seller_ed25519 = Uint256.from_json_dict(json_dict["seller_ed25519"])
        offer_id = Int64.from_json_dict(json_dict["offer_id"])
        asset_sold = Asset.from_json_dict(json_dict["asset_sold"])
        amount_sold = Int64.from_json_dict(json_dict["amount_sold"])
        asset_bought = Asset.from_json_dict(json_dict["asset_bought"])
        amount_bought = Int64.from_json_dict(json_dict["amount_bought"])
        return cls(
            seller_ed25519=seller_ed25519,
            offer_id=offer_id,
            asset_sold=asset_sold,
            amount_sold=amount_sold,
            asset_bought=asset_bought,
            amount_bought=amount_bought,
        )

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
