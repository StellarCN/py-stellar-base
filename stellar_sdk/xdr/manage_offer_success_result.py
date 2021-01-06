# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib import Packer, Unpacker

from .claim_offer_atom import ClaimOfferAtom
from .manage_offer_success_result_offer import ManageOfferSuccessResultOffer
from ..exceptions import ValueError

__all__ = ["ManageOfferSuccessResult"]


class ManageOfferSuccessResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct ManageOfferSuccessResult
    {
        // offers that got claimed while creating this offer
        ClaimOfferAtom offersClaimed<>;
    
        union switch (ManageOfferEffect effect)
        {
        case MANAGE_OFFER_CREATED:
        case MANAGE_OFFER_UPDATED:
            OfferEntry offer;
        default:
            void;
        }
        offer;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        offers_claimed: List[ClaimOfferAtom],
        offer: ManageOfferSuccessResultOffer,
    ) -> None:
        if offers_claimed and len(offers_claimed) > 4294967295:
            raise ValueError(
                f"The maximum length of `offers_claimed` should be 4294967295, but got {len(offers_claimed)}."
            )
        self.offers_claimed = offers_claimed
        self.offer = offer

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.offers_claimed))
        for offers_claimed in self.offers_claimed:
            offers_claimed.pack(packer)
        self.offer.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ManageOfferSuccessResult":
        length = unpacker.unpack_uint()
        offers_claimed = []
        for _ in range(length):
            offers_claimed.append(ClaimOfferAtom.unpack(unpacker))
        offer = ManageOfferSuccessResultOffer.unpack(unpacker)
        return cls(offers_claimed=offers_claimed, offer=offer,)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "ManageOfferSuccessResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ManageOfferSuccessResult":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.offers_claimed == other.offers_claimed and self.offer == other.offer

    def __str__(self):
        out = [
            f"offers_claimed={self.offers_claimed}",
            f"offer={self.offer}",
        ]
        return f"<ManageOfferSuccessResult {[', '.join(out)]}>"
