# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .manage_offer_effect import ManageOfferEffect
from .offer_entry import OfferEntry

__all__ = ["ManageOfferSuccessResultOffer"]


class ManageOfferSuccessResultOffer:
    """
    XDR Source Code::

        union switch (ManageOfferEffect effect)
            {
            case MANAGE_OFFER_CREATED:
            case MANAGE_OFFER_UPDATED:
                OfferEntry offer;
            case MANAGE_OFFER_DELETED:
                void;
            }
    """

    def __init__(
        self,
        effect: ManageOfferEffect,
        offer: OfferEntry = None,
    ) -> None:
        self.effect = effect
        self.offer = offer

    def pack(self, packer: Packer) -> None:
        self.effect.pack(packer)
        if self.effect == ManageOfferEffect.MANAGE_OFFER_CREATED:
            if self.offer is None:
                raise ValueError("offer should not be None.")
            self.offer.pack(packer)
            return
        if self.effect == ManageOfferEffect.MANAGE_OFFER_UPDATED:
            if self.offer is None:
                raise ValueError("offer should not be None.")
            self.offer.pack(packer)
            return
        if self.effect == ManageOfferEffect.MANAGE_OFFER_DELETED:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ManageOfferSuccessResultOffer:
        effect = ManageOfferEffect.unpack(unpacker)
        if effect == ManageOfferEffect.MANAGE_OFFER_CREATED:
            offer = OfferEntry.unpack(unpacker)
            return cls(effect=effect, offer=offer)
        if effect == ManageOfferEffect.MANAGE_OFFER_UPDATED:
            offer = OfferEntry.unpack(unpacker)
            return cls(effect=effect, offer=offer)
        if effect == ManageOfferEffect.MANAGE_OFFER_DELETED:
            return cls(effect=effect)
        return cls(effect=effect)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ManageOfferSuccessResultOffer:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ManageOfferSuccessResultOffer:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.effect,
                self.offer,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.effect == other.effect and self.offer == other.offer

    def __repr__(self):
        out = []
        out.append(f"effect={self.effect}")
        out.append(f"offer={self.offer}") if self.offer is not None else None
        return f"<ManageOfferSuccessResultOffer [{', '.join(out)}]>"
