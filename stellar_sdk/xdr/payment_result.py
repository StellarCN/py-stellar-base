# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .payment_result_code import PaymentResultCode

__all__ = ["PaymentResult"]


class PaymentResult:
    """
    XDR Source Code::

        union PaymentResult switch (PaymentResultCode code)
        {
        case PAYMENT_SUCCESS:
            void;
        case PAYMENT_MALFORMED:
        case PAYMENT_UNDERFUNDED:
        case PAYMENT_SRC_NO_TRUST:
        case PAYMENT_SRC_NOT_AUTHORIZED:
        case PAYMENT_NO_DESTINATION:
        case PAYMENT_NO_TRUST:
        case PAYMENT_NOT_AUTHORIZED:
        case PAYMENT_LINE_FULL:
        case PAYMENT_NO_ISSUER:
            void;
        };
    """

    def __init__(
        self,
        code: PaymentResultCode,
    ) -> None:
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == PaymentResultCode.PAYMENT_SUCCESS:
            return
        if self.code == PaymentResultCode.PAYMENT_MALFORMED:
            return
        if self.code == PaymentResultCode.PAYMENT_UNDERFUNDED:
            return
        if self.code == PaymentResultCode.PAYMENT_SRC_NO_TRUST:
            return
        if self.code == PaymentResultCode.PAYMENT_SRC_NOT_AUTHORIZED:
            return
        if self.code == PaymentResultCode.PAYMENT_NO_DESTINATION:
            return
        if self.code == PaymentResultCode.PAYMENT_NO_TRUST:
            return
        if self.code == PaymentResultCode.PAYMENT_NOT_AUTHORIZED:
            return
        if self.code == PaymentResultCode.PAYMENT_LINE_FULL:
            return
        if self.code == PaymentResultCode.PAYMENT_NO_ISSUER:
            return
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> PaymentResult:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        code = PaymentResultCode.unpack(unpacker)
        if code == PaymentResultCode.PAYMENT_SUCCESS:
            return cls(code=code)
        if code == PaymentResultCode.PAYMENT_MALFORMED:
            return cls(code=code)
        if code == PaymentResultCode.PAYMENT_UNDERFUNDED:
            return cls(code=code)
        if code == PaymentResultCode.PAYMENT_SRC_NO_TRUST:
            return cls(code=code)
        if code == PaymentResultCode.PAYMENT_SRC_NOT_AUTHORIZED:
            return cls(code=code)
        if code == PaymentResultCode.PAYMENT_NO_DESTINATION:
            return cls(code=code)
        if code == PaymentResultCode.PAYMENT_NO_TRUST:
            return cls(code=code)
        if code == PaymentResultCode.PAYMENT_NOT_AUTHORIZED:
            return cls(code=code)
        if code == PaymentResultCode.PAYMENT_LINE_FULL:
            return cls(code=code)
        if code == PaymentResultCode.PAYMENT_NO_ISSUER:
            return cls(code=code)
        raise ValueError("Invalid code.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> PaymentResult:
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
    def from_xdr(cls, xdr: str) -> PaymentResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> PaymentResult:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.code == PaymentResultCode.PAYMENT_SUCCESS:
            return "success"
        if self.code == PaymentResultCode.PAYMENT_MALFORMED:
            return "malformed"
        if self.code == PaymentResultCode.PAYMENT_UNDERFUNDED:
            return "underfunded"
        if self.code == PaymentResultCode.PAYMENT_SRC_NO_TRUST:
            return "src_no_trust"
        if self.code == PaymentResultCode.PAYMENT_SRC_NOT_AUTHORIZED:
            return "src_not_authorized"
        if self.code == PaymentResultCode.PAYMENT_NO_DESTINATION:
            return "no_destination"
        if self.code == PaymentResultCode.PAYMENT_NO_TRUST:
            return "no_trust"
        if self.code == PaymentResultCode.PAYMENT_NOT_AUTHORIZED:
            return "not_authorized"
        if self.code == PaymentResultCode.PAYMENT_LINE_FULL:
            return "line_full"
        if self.code == PaymentResultCode.PAYMENT_NO_ISSUER:
            return "no_issuer"
        raise ValueError(f"Unknown code in PaymentResult: {self.code}")

    @classmethod
    def from_json_dict(cls, json_value: str) -> PaymentResult:
        if json_value not in (
            "success",
            "malformed",
            "underfunded",
            "src_no_trust",
            "src_not_authorized",
            "no_destination",
            "no_trust",
            "not_authorized",
            "line_full",
            "no_issuer",
        ):
            raise ValueError(
                f"Unexpected string '{json_value}' for PaymentResult, must be one of: success, malformed, underfunded, src_no_trust, src_not_authorized, no_destination, no_trust, not_authorized, line_full, no_issuer"
            )
        code = PaymentResultCode.from_json_dict(json_value)
        return cls(code=code)

    def __hash__(self):
        return hash((self.code,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code

    def __repr__(self):
        out = []
        out.append(f"code={self.code}")
        return f"<PaymentResult [{', '.join(out)}]>"
