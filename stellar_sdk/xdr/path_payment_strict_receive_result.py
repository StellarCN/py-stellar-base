# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .asset import Asset
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
        success: PathPaymentStrictReceiveResultSuccess = None,
        no_issuer: Asset = None,
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

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> PathPaymentStrictReceiveResult:
        code = PathPaymentStrictReceiveResultCode.unpack(unpacker)
        if (
            code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_SUCCESS
        ):
            success = PathPaymentStrictReceiveResultSuccess.unpack(unpacker)
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
            no_issuer = Asset.unpack(unpacker)
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
        return cls(code=code)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> PathPaymentStrictReceiveResult:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> PathPaymentStrictReceiveResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
        out.append(f"success={self.success}") if self.success is not None else None
        (
            out.append(f"no_issuer={self.no_issuer}")
            if self.no_issuer is not None
            else None
        )
        return f"<PathPaymentStrictReceiveResult [{', '.join(out)}]>"
