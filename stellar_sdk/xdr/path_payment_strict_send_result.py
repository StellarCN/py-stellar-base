# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .asset import Asset
from .base import DEFAULT_XDR_MAX_DEPTH
from .path_payment_strict_send_result_code import PathPaymentStrictSendResultCode
from .path_payment_strict_send_result_success import PathPaymentStrictSendResultSuccess

__all__ = ["PathPaymentStrictSendResult"]


class PathPaymentStrictSendResult:
    """
    XDR Source Code::

        union PathPaymentStrictSendResult switch (PathPaymentStrictSendResultCode code)
        {
        case PATH_PAYMENT_STRICT_SEND_SUCCESS:
            struct
            {
                ClaimAtom offers<>;
                SimplePaymentResult last;
            } success;
        case PATH_PAYMENT_STRICT_SEND_MALFORMED:
        case PATH_PAYMENT_STRICT_SEND_UNDERFUNDED:
        case PATH_PAYMENT_STRICT_SEND_SRC_NO_TRUST:
        case PATH_PAYMENT_STRICT_SEND_SRC_NOT_AUTHORIZED:
        case PATH_PAYMENT_STRICT_SEND_NO_DESTINATION:
        case PATH_PAYMENT_STRICT_SEND_NO_TRUST:
        case PATH_PAYMENT_STRICT_SEND_NOT_AUTHORIZED:
        case PATH_PAYMENT_STRICT_SEND_LINE_FULL:
            void;
        case PATH_PAYMENT_STRICT_SEND_NO_ISSUER:
            Asset noIssuer; // the asset that caused the error
        case PATH_PAYMENT_STRICT_SEND_TOO_FEW_OFFERS:
        case PATH_PAYMENT_STRICT_SEND_OFFER_CROSS_SELF:
        case PATH_PAYMENT_STRICT_SEND_UNDER_DESTMIN:
            void;
        };
    """

    def __init__(
        self,
        code: PathPaymentStrictSendResultCode,
        success: Optional[PathPaymentStrictSendResultSuccess] = None,
        no_issuer: Optional[Asset] = None,
    ) -> None:
        self.code = code
        self.success = success
        self.no_issuer = no_issuer

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if (
            self.code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_SUCCESS
        ):
            if self.success is None:
                raise ValueError("success should not be None.")
            self.success.pack(packer)
            return
        if (
            self.code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_MALFORMED
        ):
            return
        if (
            self.code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_UNDERFUNDED
        ):
            return
        if (
            self.code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_SRC_NO_TRUST
        ):
            return
        if (
            self.code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_SRC_NOT_AUTHORIZED
        ):
            return
        if (
            self.code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_NO_DESTINATION
        ):
            return
        if (
            self.code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_NO_TRUST
        ):
            return
        if (
            self.code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_NOT_AUTHORIZED
        ):
            return
        if (
            self.code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_LINE_FULL
        ):
            return
        if (
            self.code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_NO_ISSUER
        ):
            if self.no_issuer is None:
                raise ValueError("no_issuer should not be None.")
            self.no_issuer.pack(packer)
            return
        if (
            self.code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_TOO_FEW_OFFERS
        ):
            return
        if (
            self.code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_OFFER_CROSS_SELF
        ):
            return
        if (
            self.code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_UNDER_DESTMIN
        ):
            return
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> PathPaymentStrictSendResult:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        code = PathPaymentStrictSendResultCode.unpack(unpacker)
        if code == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_SUCCESS:
            success = PathPaymentStrictSendResultSuccess.unpack(
                unpacker, depth_limit - 1
            )
            return cls(code=code, success=success)
        if code == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_MALFORMED:
            return cls(code=code)
        if code == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_UNDERFUNDED:
            return cls(code=code)
        if (
            code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_SRC_NO_TRUST
        ):
            return cls(code=code)
        if (
            code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_SRC_NOT_AUTHORIZED
        ):
            return cls(code=code)
        if (
            code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_NO_DESTINATION
        ):
            return cls(code=code)
        if code == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_NO_TRUST:
            return cls(code=code)
        if (
            code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_NOT_AUTHORIZED
        ):
            return cls(code=code)
        if code == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_LINE_FULL:
            return cls(code=code)
        if code == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_NO_ISSUER:
            no_issuer = Asset.unpack(unpacker, depth_limit - 1)
            return cls(code=code, no_issuer=no_issuer)
        if (
            code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_TOO_FEW_OFFERS
        ):
            return cls(code=code)
        if (
            code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_OFFER_CROSS_SELF
        ):
            return cls(code=code)
        if (
            code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_UNDER_DESTMIN
        ):
            return cls(code=code)
        raise ValueError("Invalid code.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> PathPaymentStrictSendResult:
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
    def from_xdr(cls, xdr: str) -> PathPaymentStrictSendResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> PathPaymentStrictSendResult:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if (
            self.code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_SUCCESS
        ):
            assert self.success is not None
            return {"success": self.success.to_json_dict()}
        if (
            self.code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_MALFORMED
        ):
            return "malformed"
        if (
            self.code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_UNDERFUNDED
        ):
            return "underfunded"
        if (
            self.code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_SRC_NO_TRUST
        ):
            return "src_no_trust"
        if (
            self.code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_SRC_NOT_AUTHORIZED
        ):
            return "src_not_authorized"
        if (
            self.code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_NO_DESTINATION
        ):
            return "no_destination"
        if (
            self.code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_NO_TRUST
        ):
            return "no_trust"
        if (
            self.code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_NOT_AUTHORIZED
        ):
            return "not_authorized"
        if (
            self.code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_LINE_FULL
        ):
            return "line_full"
        if (
            self.code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_NO_ISSUER
        ):
            assert self.no_issuer is not None
            return {"no_issuer": self.no_issuer.to_json_dict()}
        if (
            self.code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_TOO_FEW_OFFERS
        ):
            return "too_few_offers"
        if (
            self.code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_OFFER_CROSS_SELF
        ):
            return "offer_cross_self"
        if (
            self.code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_UNDER_DESTMIN
        ):
            return "under_destmin"
        raise ValueError(f"Unknown code in PathPaymentStrictSendResult: {self.code}")

    @classmethod
    def from_json_dict(cls, json_value: str | dict) -> PathPaymentStrictSendResult:
        if isinstance(json_value, str):
            if json_value not in (
                "malformed",
                "underfunded",
                "src_no_trust",
                "src_not_authorized",
                "no_destination",
                "no_trust",
                "not_authorized",
                "line_full",
                "too_few_offers",
                "offer_cross_self",
                "under_destmin",
            ):
                raise ValueError(
                    f"Unexpected string '{json_value}' for PathPaymentStrictSendResult, must be one of: malformed, underfunded, src_no_trust, src_not_authorized, no_destination, no_trust, not_authorized, line_full, too_few_offers, offer_cross_self, under_destmin"
                )
            code = PathPaymentStrictSendResultCode.from_json_dict(json_value)
            return cls(code=code)
        if not isinstance(json_value, dict) or len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for PathPaymentStrictSendResult, got: {json_value}"
            )
        key = next(iter(json_value))
        code = PathPaymentStrictSendResultCode.from_json_dict(key)
        if key == "success":
            success = PathPaymentStrictSendResultSuccess.from_json_dict(
                json_value["success"]
            )
            return cls(code=code, success=success)
        if key == "no_issuer":
            no_issuer = Asset.from_json_dict(json_value["no_issuer"])
            return cls(code=code, no_issuer=no_issuer)
        raise ValueError(f"Unknown key '{key}' for PathPaymentStrictSendResult")

    def __hash__(self):
        return hash(
            (
                self.code,
                self.success,
                self.no_issuer,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.code == other.code
            and self.success == other.success
            and self.no_issuer == other.no_issuer
        )

    def __repr__(self):
        out = []
        out.append(f"code={self.code}")
        if self.success is not None:
            out.append(f"success={self.success}")
        if self.no_issuer is not None:
            out.append(f"no_issuer={self.no_issuer}")
        return f"<PathPaymentStrictSendResult [{', '.join(out)}]>"
