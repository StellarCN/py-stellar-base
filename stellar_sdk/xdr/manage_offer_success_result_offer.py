# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
        offer: Optional[OfferEntry] = None,
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
        raise ValueError("Invalid effect.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ManageOfferSuccessResultOffer:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        effect = ManageOfferEffect.unpack(unpacker)
        if effect == ManageOfferEffect.MANAGE_OFFER_CREATED:
            offer = OfferEntry.unpack(unpacker, depth_limit - 1)
            return cls(effect=effect, offer=offer)
        if effect == ManageOfferEffect.MANAGE_OFFER_UPDATED:
            offer = OfferEntry.unpack(unpacker, depth_limit - 1)
            return cls(effect=effect, offer=offer)
        if effect == ManageOfferEffect.MANAGE_OFFER_DELETED:
            return cls(effect=effect)
        raise ValueError("Invalid effect.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ManageOfferSuccessResultOffer:
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
    def from_xdr(cls, xdr: str) -> ManageOfferSuccessResultOffer:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ManageOfferSuccessResultOffer:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.effect == ManageOfferEffect.MANAGE_OFFER_CREATED:
            assert self.offer is not None
            return {"created": self.offer.to_json_dict()}
        if self.effect == ManageOfferEffect.MANAGE_OFFER_UPDATED:
            assert self.offer is not None
            return {"updated": self.offer.to_json_dict()}
        if self.effect == ManageOfferEffect.MANAGE_OFFER_DELETED:
            return "deleted"
        raise ValueError(
            f"Unknown effect in ManageOfferSuccessResultOffer: {self.effect}"
        )

    @classmethod
    def from_json_dict(cls, json_value: str | dict) -> ManageOfferSuccessResultOffer:
        if isinstance(json_value, str):
            if json_value not in ("deleted",):
                raise ValueError(
                    f"Unexpected string '{json_value}' for ManageOfferSuccessResultOffer, must be one of: deleted"
                )
            effect = ManageOfferEffect.from_json_dict(json_value)
            return cls(effect=effect)
        if not isinstance(json_value, dict) or len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for ManageOfferSuccessResultOffer, got: {json_value}"
            )
        key = next(iter(json_value))
        effect = ManageOfferEffect.from_json_dict(key)
        if key == "created":
            offer = OfferEntry.from_json_dict(json_value["created"])
            return cls(effect=effect, offer=offer)
        if key == "updated":
            offer = OfferEntry.from_json_dict(json_value["updated"])
            return cls(effect=effect, offer=offer)
        raise ValueError(f"Unknown key '{key}' for ManageOfferSuccessResultOffer")

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
        if self.offer is not None:
            out.append(f"offer={self.offer}")
        return f"<ManageOfferSuccessResultOffer [{', '.join(out)}]>"
