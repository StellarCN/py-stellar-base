# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_PAYMENT_RESULT_CODE_MAP = {
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
}
_PAYMENT_RESULT_CODE_REVERSE_MAP = {
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
}
__all__ = ["PaymentResultCode"]


class PaymentResultCode(IntEnum):
    """
    XDR Source Code::

        enum PaymentResultCode
        {
            // codes considered as "success" for the operation
            PAYMENT_SUCCESS = 0, // payment successfully completed

            // codes considered as "failure" for the operation
            PAYMENT_MALFORMED = -1,          // bad input
            PAYMENT_UNDERFUNDED = -2,        // not enough funds in source account
            PAYMENT_SRC_NO_TRUST = -3,       // no trust line on source account
            PAYMENT_SRC_NOT_AUTHORIZED = -4, // source not authorized to transfer
            PAYMENT_NO_DESTINATION = -5,     // destination account does not exist
            PAYMENT_NO_TRUST = -6,       // destination missing a trust line for asset
            PAYMENT_NOT_AUTHORIZED = -7, // destination not authorized to hold asset
            PAYMENT_LINE_FULL = -8,      // destination would go above their limit
            PAYMENT_NO_ISSUER = -9       // missing issuer on asset
        };
    """

    PAYMENT_SUCCESS = 0
    PAYMENT_MALFORMED = -1
    PAYMENT_UNDERFUNDED = -2
    PAYMENT_SRC_NO_TRUST = -3
    PAYMENT_SRC_NOT_AUTHORIZED = -4
    PAYMENT_NO_DESTINATION = -5
    PAYMENT_NO_TRUST = -6
    PAYMENT_NOT_AUTHORIZED = -7
    PAYMENT_LINE_FULL = -8
    PAYMENT_NO_ISSUER = -9

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> PaymentResultCode:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> PaymentResultCode:
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
    def from_xdr(cls, xdr: str) -> PaymentResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> PaymentResultCode:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _PAYMENT_RESULT_CODE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> PaymentResultCode:
        return cls(_PAYMENT_RESULT_CODE_REVERSE_MAP[json_value])
