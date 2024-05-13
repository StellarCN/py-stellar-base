# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

from .claim_atom import ClaimAtom
from .manage_offer_success_result_offer import ManageOfferSuccessResultOffer

__all__ = ["ManageOfferSuccessResult"]


class ManageOfferSuccessResult:
    """
    XDR Source Code::

        struct ManageOfferSuccessResult
        {
            // offers that got claimed while creating this offer
            ClaimAtom offersClaimed<>;

            union switch (ManageOfferEffect effect)
            {
            case MANAGE_OFFER_CREATED:
            case MANAGE_OFFER_UPDATED:
                OfferEntry offer;
            case MANAGE_OFFER_DELETED:
                void;
            }
            offer;
        };
    """

    def __init__(
        self,
        offers_claimed: List[ClaimAtom],
        offer: ManageOfferSuccessResultOffer,
    ) -> None:
        _expect_max_length = 4294967295
        if offers_claimed and len(offers_claimed) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `offers_claimed` should be {_expect_max_length}, but got {len(offers_claimed)}."
            )
        self.offers_claimed = offers_claimed
        self.offer = offer

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.offers_claimed))
        for offers_claimed_item in self.offers_claimed:
            offers_claimed_item.pack(packer)
        self.offer.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ManageOfferSuccessResult:
        length = unpacker.unpack_uint()
        offers_claimed = []
        for _ in range(length):
            offers_claimed.append(ClaimAtom.unpack(unpacker))
        offer = ManageOfferSuccessResultOffer.unpack(unpacker)
        return cls(
            offers_claimed=offers_claimed,
            offer=offer,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ManageOfferSuccessResult:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ManageOfferSuccessResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.offers_claimed,
                self.offer,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.offers_claimed == other.offers_claimed and self.offer == other.offer

    def __repr__(self):
        out = [
            f"offers_claimed={self.offers_claimed}",
            f"offer={self.offer}",
        ]
        return f"<ManageOfferSuccessResult [{', '.join(out)}]>"
