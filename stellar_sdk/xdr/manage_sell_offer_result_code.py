# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

__all__ = ["ManageSellOfferResultCode"]


class ManageSellOfferResultCode(IntEnum):
    """
    XDR Source Code::

        enum ManageSellOfferResultCode
        {
            // codes considered as "success" for the operation
            MANAGE_SELL_OFFER_SUCCESS = 0,

            // codes considered as "failure" for the operation
            MANAGE_SELL_OFFER_MALFORMED = -1, // generated offer would be invalid
            MANAGE_SELL_OFFER_SELL_NO_TRUST =
                -2,                              // no trust line for what we're selling
            MANAGE_SELL_OFFER_BUY_NO_TRUST = -3, // no trust line for what we're buying
            MANAGE_SELL_OFFER_SELL_NOT_AUTHORIZED = -4, // not authorized to sell
            MANAGE_SELL_OFFER_BUY_NOT_AUTHORIZED = -5,  // not authorized to buy
            MANAGE_SELL_OFFER_LINE_FULL = -6, // can't receive more of what it's buying
            MANAGE_SELL_OFFER_UNDERFUNDED = -7, // doesn't hold what it's trying to sell
            MANAGE_SELL_OFFER_CROSS_SELF =
                -8, // would cross an offer from the same user
            MANAGE_SELL_OFFER_SELL_NO_ISSUER = -9, // no issuer for what we're selling
            MANAGE_SELL_OFFER_BUY_NO_ISSUER = -10, // no issuer for what we're buying

            // update errors
            MANAGE_SELL_OFFER_NOT_FOUND =
                -11, // offerID does not match an existing offer

            MANAGE_SELL_OFFER_LOW_RESERVE =
                -12 // not enough funds to create a new Offer
        };
    """

    MANAGE_SELL_OFFER_SUCCESS = 0
    MANAGE_SELL_OFFER_MALFORMED = -1
    MANAGE_SELL_OFFER_SELL_NO_TRUST = -2
    MANAGE_SELL_OFFER_BUY_NO_TRUST = -3
    MANAGE_SELL_OFFER_SELL_NOT_AUTHORIZED = -4
    MANAGE_SELL_OFFER_BUY_NOT_AUTHORIZED = -5
    MANAGE_SELL_OFFER_LINE_FULL = -6
    MANAGE_SELL_OFFER_UNDERFUNDED = -7
    MANAGE_SELL_OFFER_CROSS_SELF = -8
    MANAGE_SELL_OFFER_SELL_NO_ISSUER = -9
    MANAGE_SELL_OFFER_BUY_NO_ISSUER = -10
    MANAGE_SELL_OFFER_NOT_FOUND = -11
    MANAGE_SELL_OFFER_LOW_RESERVE = -12

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ManageSellOfferResultCode:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ManageSellOfferResultCode:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ManageSellOfferResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
