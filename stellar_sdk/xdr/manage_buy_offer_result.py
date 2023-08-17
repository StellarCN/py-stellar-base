# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

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
        success: ManageOfferSuccessResult = None,
    ) -> None:
        self.code = code
        self.success = success

    @classmethod
    def from_manage_buy_offer_success(
        cls, success: ManageOfferSuccessResult
    ) -> ManageBuyOfferResult:
        return cls(ManageBuyOfferResultCode.MANAGE_BUY_OFFER_SUCCESS, success=success)

    @classmethod
    def from_manage_buy_offer_malformed(cls) -> ManageBuyOfferResult:
        return cls(ManageBuyOfferResultCode.MANAGE_BUY_OFFER_MALFORMED)

    @classmethod
    def from_manage_buy_offer_sell_no_trust(cls) -> ManageBuyOfferResult:
        return cls(ManageBuyOfferResultCode.MANAGE_BUY_OFFER_SELL_NO_TRUST)

    @classmethod
    def from_manage_buy_offer_buy_no_trust(cls) -> ManageBuyOfferResult:
        return cls(ManageBuyOfferResultCode.MANAGE_BUY_OFFER_BUY_NO_TRUST)

    @classmethod
    def from_manage_buy_offer_sell_not_authorized(cls) -> ManageBuyOfferResult:
        return cls(ManageBuyOfferResultCode.MANAGE_BUY_OFFER_SELL_NOT_AUTHORIZED)

    @classmethod
    def from_manage_buy_offer_buy_not_authorized(cls) -> ManageBuyOfferResult:
        return cls(ManageBuyOfferResultCode.MANAGE_BUY_OFFER_BUY_NOT_AUTHORIZED)

    @classmethod
    def from_manage_buy_offer_line_full(cls) -> ManageBuyOfferResult:
        return cls(ManageBuyOfferResultCode.MANAGE_BUY_OFFER_LINE_FULL)

    @classmethod
    def from_manage_buy_offer_underfunded(cls) -> ManageBuyOfferResult:
        return cls(ManageBuyOfferResultCode.MANAGE_BUY_OFFER_UNDERFUNDED)

    @classmethod
    def from_manage_buy_offer_cross_self(cls) -> ManageBuyOfferResult:
        return cls(ManageBuyOfferResultCode.MANAGE_BUY_OFFER_CROSS_SELF)

    @classmethod
    def from_manage_buy_offer_sell_no_issuer(cls) -> ManageBuyOfferResult:
        return cls(ManageBuyOfferResultCode.MANAGE_BUY_OFFER_SELL_NO_ISSUER)

    @classmethod
    def from_manage_buy_offer_buy_no_issuer(cls) -> ManageBuyOfferResult:
        return cls(ManageBuyOfferResultCode.MANAGE_BUY_OFFER_BUY_NO_ISSUER)

    @classmethod
    def from_manage_buy_offer_not_found(cls) -> ManageBuyOfferResult:
        return cls(ManageBuyOfferResultCode.MANAGE_BUY_OFFER_NOT_FOUND)

    @classmethod
    def from_manage_buy_offer_low_reserve(cls) -> ManageBuyOfferResult:
        return cls(ManageBuyOfferResultCode.MANAGE_BUY_OFFER_LOW_RESERVE)

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

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ManageBuyOfferResult:
        code = ManageBuyOfferResultCode.unpack(unpacker)
        if code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_SUCCESS:
            success = ManageOfferSuccessResult.unpack(unpacker)
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
        return cls(code=code)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ManageBuyOfferResult:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ManageBuyOfferResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code and self.success == other.success

    def __str__(self):
        out = []
        out.append(f"code={self.code}")
        out.append(f"success={self.success}") if self.success is not None else None
        return f"<ManageBuyOfferResult [{', '.join(out)}]>"
