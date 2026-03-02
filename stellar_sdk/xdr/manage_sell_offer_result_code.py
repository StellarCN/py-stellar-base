# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_MANAGE_SELL_OFFER_RESULT_CODE_MAP = {
    0: "success",
    -1: "malformed",
    -2: "sell_no_trust",
    -3: "buy_no_trust",
    -4: "sell_not_authorized",
    -5: "buy_not_authorized",
    -6: "line_full",
    -7: "underfunded",
    -8: "cross_self",
    -9: "sell_no_issuer",
    -10: "buy_no_issuer",
    -11: "not_found",
    -12: "low_reserve",
}
_MANAGE_SELL_OFFER_RESULT_CODE_REVERSE_MAP = {
    "success": 0,
    "malformed": -1,
    "sell_no_trust": -2,
    "buy_no_trust": -3,
    "sell_not_authorized": -4,
    "buy_not_authorized": -5,
    "line_full": -6,
    "underfunded": -7,
    "cross_self": -8,
    "sell_no_issuer": -9,
    "buy_no_issuer": -10,
    "not_found": -11,
    "low_reserve": -12,
}
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ManageSellOfferResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ManageSellOfferResultCode:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _MANAGE_SELL_OFFER_RESULT_CODE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> ManageSellOfferResultCode:
        return cls(_MANAGE_SELL_OFFER_RESULT_CODE_REVERSE_MAP[json_value])
