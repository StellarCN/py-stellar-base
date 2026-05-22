# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_PATH_PAYMENT_STRICT_RECEIVE_RESULT_CODE_MAP = {
    0: "success",
    -1: "malformed",
    -2: "underfunded",
    -3: "src_no_trust",
    -4: "src_not_authorized",
    -5: "no_destination",
    -6: "no_trust",
    -7: "not_authorized",
    -8: "line_full",
    -9: "no_issuer",
    -10: "too_few_offers",
    -11: "offer_cross_self",
    -12: "over_sendmax",
}
_PATH_PAYMENT_STRICT_RECEIVE_RESULT_CODE_REVERSE_MAP = {
    "success": 0,
    "malformed": -1,
    "underfunded": -2,
    "src_no_trust": -3,
    "src_not_authorized": -4,
    "no_destination": -5,
    "no_trust": -6,
    "not_authorized": -7,
    "line_full": -8,
    "no_issuer": -9,
    "too_few_offers": -10,
    "offer_cross_self": -11,
    "over_sendmax": -12,
}
__all__ = ["PathPaymentStrictReceiveResultCode"]


class PathPaymentStrictReceiveResultCode(IntEnum):
    """
    XDR Source Code::

        enum PathPaymentStrictReceiveResultCode
        {
            // codes considered as "success" for the operation
            PATH_PAYMENT_STRICT_RECEIVE_SUCCESS = 0, // success

            // codes considered as "failure" for the operation
            PATH_PAYMENT_STRICT_RECEIVE_MALFORMED = -1, // bad input
            PATH_PAYMENT_STRICT_RECEIVE_UNDERFUNDED =
                -2, // not enough funds in source account
            PATH_PAYMENT_STRICT_RECEIVE_SRC_NO_TRUST =
                -3, // no trust line on source account
            PATH_PAYMENT_STRICT_RECEIVE_SRC_NOT_AUTHORIZED =
                -4, // source not authorized to transfer
            PATH_PAYMENT_STRICT_RECEIVE_NO_DESTINATION =
                -5, // destination account does not exist
            PATH_PAYMENT_STRICT_RECEIVE_NO_TRUST =
                -6, // dest missing a trust line for asset
            PATH_PAYMENT_STRICT_RECEIVE_NOT_AUTHORIZED =
                -7, // dest not authorized to hold asset
            PATH_PAYMENT_STRICT_RECEIVE_LINE_FULL =
                -8, // dest would go above their limit
            PATH_PAYMENT_STRICT_RECEIVE_NO_ISSUER = -9, // missing issuer on one asset
            PATH_PAYMENT_STRICT_RECEIVE_TOO_FEW_OFFERS =
                -10, // not enough offers to satisfy path
            PATH_PAYMENT_STRICT_RECEIVE_OFFER_CROSS_SELF =
                -11, // would cross one of its own offers
            PATH_PAYMENT_STRICT_RECEIVE_OVER_SENDMAX = -12 // could not satisfy sendmax
        };
    """

    PATH_PAYMENT_STRICT_RECEIVE_SUCCESS = 0
    PATH_PAYMENT_STRICT_RECEIVE_MALFORMED = -1
    PATH_PAYMENT_STRICT_RECEIVE_UNDERFUNDED = -2
    PATH_PAYMENT_STRICT_RECEIVE_SRC_NO_TRUST = -3
    PATH_PAYMENT_STRICT_RECEIVE_SRC_NOT_AUTHORIZED = -4
    PATH_PAYMENT_STRICT_RECEIVE_NO_DESTINATION = -5
    PATH_PAYMENT_STRICT_RECEIVE_NO_TRUST = -6
    PATH_PAYMENT_STRICT_RECEIVE_NOT_AUTHORIZED = -7
    PATH_PAYMENT_STRICT_RECEIVE_LINE_FULL = -8
    PATH_PAYMENT_STRICT_RECEIVE_NO_ISSUER = -9
    PATH_PAYMENT_STRICT_RECEIVE_TOO_FEW_OFFERS = -10
    PATH_PAYMENT_STRICT_RECEIVE_OFFER_CROSS_SELF = -11
    PATH_PAYMENT_STRICT_RECEIVE_OVER_SENDMAX = -12

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> PathPaymentStrictReceiveResultCode:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> PathPaymentStrictReceiveResultCode:
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
    def from_xdr(cls, xdr: str) -> PathPaymentStrictReceiveResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> PathPaymentStrictReceiveResultCode:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _PATH_PAYMENT_STRICT_RECEIVE_RESULT_CODE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> PathPaymentStrictReceiveResultCode:
        return cls(_PATH_PAYMENT_STRICT_RECEIVE_RESULT_CODE_REVERSE_MAP[json_value])
