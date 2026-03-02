# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .manage_buy_offer_result_code import ManageBuyOfferResultCode
from .manage_offer_success_result import ManageOfferSuccessResult

__all__ = ["ManageBuyOfferResult"]


class ManageBuyOfferResult:
    """
    XDR Source Code::

        union ManageBuyOfferResult switch (ManageBuyOfferResultCode code)
        {
        case MANAGE_BUY_OFFER_SUCCESS:
            ManageOfferSuccessResult success;
        case MANAGE_BUY_OFFER_MALFORMED:
        case MANAGE_BUY_OFFER_SELL_NO_TRUST:
        case MANAGE_BUY_OFFER_BUY_NO_TRUST:
        case MANAGE_BUY_OFFER_SELL_NOT_AUTHORIZED:
        case MANAGE_BUY_OFFER_BUY_NOT_AUTHORIZED:
        case MANAGE_BUY_OFFER_LINE_FULL:
        case MANAGE_BUY_OFFER_UNDERFUNDED:
        case MANAGE_BUY_OFFER_CROSS_SELF:
        case MANAGE_BUY_OFFER_SELL_NO_ISSUER:
        case MANAGE_BUY_OFFER_BUY_NO_ISSUER:
        case MANAGE_BUY_OFFER_NOT_FOUND:
        case MANAGE_BUY_OFFER_LOW_RESERVE:
            void;
        };
    """

    def __init__(
        self,
        code: ManageBuyOfferResultCode,
        success: Optional[ManageOfferSuccessResult] = None,
    ) -> None:
        self.code = code
        self.success = success

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_SUCCESS:
            if self.success is None:
                raise ValueError("success should not be None.")
            self.success.pack(packer)
            return
        if self.code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_MALFORMED:
            return
        if self.code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_SELL_NO_TRUST:
            return
        if self.code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_BUY_NO_TRUST:
            return
        if self.code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_SELL_NOT_AUTHORIZED:
            return
        if self.code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_BUY_NOT_AUTHORIZED:
            return
        if self.code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_LINE_FULL:
            return
        if self.code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_UNDERFUNDED:
            return
        if self.code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_CROSS_SELF:
            return
        if self.code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_SELL_NO_ISSUER:
            return
        if self.code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_BUY_NO_ISSUER:
            return
        if self.code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_NOT_FOUND:
            return
        if self.code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_LOW_RESERVE:
            return
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ManageBuyOfferResult:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        code = ManageBuyOfferResultCode.unpack(unpacker)
        if code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_SUCCESS:
            success = ManageOfferSuccessResult.unpack(unpacker, depth_limit - 1)
            return cls(code=code, success=success)
        if code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_MALFORMED:
            return cls(code=code)
        if code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_SELL_NO_TRUST:
            return cls(code=code)
        if code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_BUY_NO_TRUST:
            return cls(code=code)
        if code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_SELL_NOT_AUTHORIZED:
            return cls(code=code)
        if code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_BUY_NOT_AUTHORIZED:
            return cls(code=code)
        if code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_LINE_FULL:
            return cls(code=code)
        if code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_UNDERFUNDED:
            return cls(code=code)
        if code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_CROSS_SELF:
            return cls(code=code)
        if code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_SELL_NO_ISSUER:
            return cls(code=code)
        if code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_BUY_NO_ISSUER:
            return cls(code=code)
        if code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_NOT_FOUND:
            return cls(code=code)
        if code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_LOW_RESERVE:
            return cls(code=code)
        raise ValueError("Invalid code.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ManageBuyOfferResult:
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
    def from_xdr(cls, xdr: str) -> ManageBuyOfferResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ManageBuyOfferResult:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_SUCCESS:
            assert self.success is not None
            return {"success": self.success.to_json_dict()}
        if self.code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_MALFORMED:
            return "malformed"
        if self.code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_SELL_NO_TRUST:
            return "sell_no_trust"
        if self.code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_BUY_NO_TRUST:
            return "buy_no_trust"
        if self.code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_SELL_NOT_AUTHORIZED:
            return "sell_not_authorized"
        if self.code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_BUY_NOT_AUTHORIZED:
            return "buy_not_authorized"
        if self.code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_LINE_FULL:
            return "line_full"
        if self.code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_UNDERFUNDED:
            return "underfunded"
        if self.code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_CROSS_SELF:
            return "cross_self"
        if self.code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_SELL_NO_ISSUER:
            return "sell_no_issuer"
        if self.code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_BUY_NO_ISSUER:
            return "buy_no_issuer"
        if self.code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_NOT_FOUND:
            return "not_found"
        if self.code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_LOW_RESERVE:
            return "low_reserve"
        raise ValueError(f"Unknown code in ManageBuyOfferResult: {self.code}")

    @classmethod
    def from_json_dict(cls, json_value: str | dict) -> ManageBuyOfferResult:
        if isinstance(json_value, str):
            if json_value not in (
                "malformed",
                "sell_no_trust",
                "buy_no_trust",
                "sell_not_authorized",
                "buy_not_authorized",
                "line_full",
                "underfunded",
                "cross_self",
                "sell_no_issuer",
                "buy_no_issuer",
                "not_found",
                "low_reserve",
            ):
                raise ValueError(
                    f"Unexpected string '{json_value}' for ManageBuyOfferResult, must be one of: malformed, sell_no_trust, buy_no_trust, sell_not_authorized, buy_not_authorized, line_full, underfunded, cross_self, sell_no_issuer, buy_no_issuer, not_found, low_reserve"
                )
            code = ManageBuyOfferResultCode.from_json_dict(json_value)
            return cls(code=code)
        if not isinstance(json_value, dict) or len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for ManageBuyOfferResult, got: {json_value}"
            )
        key = next(iter(json_value))
        code = ManageBuyOfferResultCode.from_json_dict(key)
        if key == "success":
            success = ManageOfferSuccessResult.from_json_dict(json_value["success"])
            return cls(code=code, success=success)
        raise ValueError(f"Unknown key '{key}' for ManageBuyOfferResult")

    def __hash__(self):
        return hash(
            (
                self.code,
                self.success,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code and self.success == other.success

    def __repr__(self):
        out = []
        out.append(f"code={self.code}")
        if self.success is not None:
            out.append(f"success={self.success}")
        return f"<ManageBuyOfferResult [{', '.join(out)}]>"
