# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .asset import Asset
from .base import DEFAULT_XDR_MAX_DEPTH
from .path_payment_strict_receive_result_code import PathPaymentStrictReceiveResultCode
from .path_payment_strict_receive_result_success import (
    PathPaymentStrictReceiveResultSuccess,
)

__all__ = ["PathPaymentStrictReceiveResult"]


class PathPaymentStrictReceiveResult:
    """
    XDR Source Code::

        union PathPaymentStrictReceiveResult switch (
            PathPaymentStrictReceiveResultCode code)
        {
        case PATH_PAYMENT_STRICT_RECEIVE_SUCCESS:
            struct
            {
                ClaimAtom offers<>;
                SimplePaymentResult last;
            } success;
        case PATH_PAYMENT_STRICT_RECEIVE_MALFORMED:
        case PATH_PAYMENT_STRICT_RECEIVE_UNDERFUNDED:
        case PATH_PAYMENT_STRICT_RECEIVE_SRC_NO_TRUST:
        case PATH_PAYMENT_STRICT_RECEIVE_SRC_NOT_AUTHORIZED:
        case PATH_PAYMENT_STRICT_RECEIVE_NO_DESTINATION:
        case PATH_PAYMENT_STRICT_RECEIVE_NO_TRUST:
        case PATH_PAYMENT_STRICT_RECEIVE_NOT_AUTHORIZED:
        case PATH_PAYMENT_STRICT_RECEIVE_LINE_FULL:
            void;
        case PATH_PAYMENT_STRICT_RECEIVE_NO_ISSUER:
            Asset noIssuer; // the asset that caused the error
        case PATH_PAYMENT_STRICT_RECEIVE_TOO_FEW_OFFERS:
        case PATH_PAYMENT_STRICT_RECEIVE_OFFER_CROSS_SELF:
        case PATH_PAYMENT_STRICT_RECEIVE_OVER_SENDMAX:
            void;
        };
    """

    def __init__(
        self,
        code: PathPaymentStrictReceiveResultCode,
        success: Optional[PathPaymentStrictReceiveResultSuccess] = None,
        no_issuer: Optional[Asset] = None,
    ) -> None:
        self.code = code
        self.success = success
        self.no_issuer = no_issuer

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if (
            self.code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_SUCCESS
        ):
            if self.success is None:
                raise ValueError("success should not be None.")
            self.success.pack(packer)
            return
        if (
            self.code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_MALFORMED
        ):
            return
        if (
            self.code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_UNDERFUNDED
        ):
            return
        if (
            self.code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_SRC_NO_TRUST
        ):
            return
        if (
            self.code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_SRC_NOT_AUTHORIZED
        ):
            return
        if (
            self.code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_NO_DESTINATION
        ):
            return
        if (
            self.code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_NO_TRUST
        ):
            return
        if (
            self.code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_NOT_AUTHORIZED
        ):
            return
        if (
            self.code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_LINE_FULL
        ):
            return
        if (
            self.code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_NO_ISSUER
        ):
            if self.no_issuer is None:
                raise ValueError("no_issuer should not be None.")
            self.no_issuer.pack(packer)
            return
        if (
            self.code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_TOO_FEW_OFFERS
        ):
            return
        if (
            self.code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_OFFER_CROSS_SELF
        ):
            return
        if (
            self.code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_OVER_SENDMAX
        ):
            return
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> PathPaymentStrictReceiveResult:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        code = PathPaymentStrictReceiveResultCode.unpack(unpacker)
        if (
            code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_SUCCESS
        ):
            success = PathPaymentStrictReceiveResultSuccess.unpack(
                unpacker, depth_limit - 1
            )
            return cls(code=code, success=success)
        if (
            code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_MALFORMED
        ):
            return cls(code=code)
        if (
            code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_UNDERFUNDED
        ):
            return cls(code=code)
        if (
            code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_SRC_NO_TRUST
        ):
            return cls(code=code)
        if (
            code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_SRC_NOT_AUTHORIZED
        ):
            return cls(code=code)
        if (
            code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_NO_DESTINATION
        ):
            return cls(code=code)
        if (
            code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_NO_TRUST
        ):
            return cls(code=code)
        if (
            code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_NOT_AUTHORIZED
        ):
            return cls(code=code)
        if (
            code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_LINE_FULL
        ):
            return cls(code=code)
        if (
            code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_NO_ISSUER
        ):
            no_issuer = Asset.unpack(unpacker, depth_limit - 1)
            return cls(code=code, no_issuer=no_issuer)
        if (
            code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_TOO_FEW_OFFERS
        ):
            return cls(code=code)
        if (
            code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_OFFER_CROSS_SELF
        ):
            return cls(code=code)
        if (
            code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_OVER_SENDMAX
        ):
            return cls(code=code)
        raise ValueError("Invalid code.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> PathPaymentStrictReceiveResult:
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
    def from_xdr(cls, xdr: str) -> PathPaymentStrictReceiveResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> PathPaymentStrictReceiveResult:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if (
            self.code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_SUCCESS
        ):
            assert self.success is not None
            return {"success": self.success.to_json_dict()}
        if (
            self.code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_MALFORMED
        ):
            return "malformed"
        if (
            self.code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_UNDERFUNDED
        ):
            return "underfunded"
        if (
            self.code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_SRC_NO_TRUST
        ):
            return "src_no_trust"
        if (
            self.code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_SRC_NOT_AUTHORIZED
        ):
            return "src_not_authorized"
        if (
            self.code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_NO_DESTINATION
        ):
            return "no_destination"
        if (
            self.code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_NO_TRUST
        ):
            return "no_trust"
        if (
            self.code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_NOT_AUTHORIZED
        ):
            return "not_authorized"
        if (
            self.code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_LINE_FULL
        ):
            return "line_full"
        if (
            self.code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_NO_ISSUER
        ):
            assert self.no_issuer is not None
            return {"no_issuer": self.no_issuer.to_json_dict()}
        if (
            self.code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_TOO_FEW_OFFERS
        ):
            return "too_few_offers"
        if (
            self.code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_OFFER_CROSS_SELF
        ):
            return "offer_cross_self"
        if (
            self.code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_OVER_SENDMAX
        ):
            return "over_sendmax"
        raise ValueError(f"Unknown code in PathPaymentStrictReceiveResult: {self.code}")

    @classmethod
    def from_json_dict(cls, json_value: str | dict) -> PathPaymentStrictReceiveResult:
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
                "over_sendmax",
            ):
                raise ValueError(
                    f"Unexpected string '{json_value}' for PathPaymentStrictReceiveResult, must be one of: malformed, underfunded, src_no_trust, src_not_authorized, no_destination, no_trust, not_authorized, line_full, too_few_offers, offer_cross_self, over_sendmax"
                )
            code = PathPaymentStrictReceiveResultCode.from_json_dict(json_value)
            return cls(code=code)
        if not isinstance(json_value, dict) or len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for PathPaymentStrictReceiveResult, got: {json_value}"
            )
        key = next(iter(json_value))
        code = PathPaymentStrictReceiveResultCode.from_json_dict(key)
        if key == "success":
            success = PathPaymentStrictReceiveResultSuccess.from_json_dict(
                json_value["success"]
            )
            return cls(code=code, success=success)
        if key == "no_issuer":
            no_issuer = Asset.from_json_dict(json_value["no_issuer"])
            return cls(code=code, no_issuer=no_issuer)
        raise ValueError(f"Unknown key '{key}' for PathPaymentStrictReceiveResult")

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
        return f"<PathPaymentStrictReceiveResult [{', '.join(out)}]>"
