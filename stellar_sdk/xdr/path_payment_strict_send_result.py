# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib3 import Packer, Unpacker

from .asset import Asset
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
        success: PathPaymentStrictSendResultSuccess = None,
        no_issuer: Asset = None,
    ) -> None:
        self.code = code
        self.success = success
        self.no_issuer = no_issuer

    @classmethod
    def from_path_payment_strict_send_success(
        cls, success: PathPaymentStrictSendResultSuccess
    ) -> "PathPaymentStrictSendResult":
        return cls(
            PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_SUCCESS,
            success=success,
        )

    @classmethod
    def from_path_payment_strict_send_malformed(cls) -> "PathPaymentStrictSendResult":
        return cls(PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_MALFORMED)

    @classmethod
    def from_path_payment_strict_send_underfunded(cls) -> "PathPaymentStrictSendResult":
        return cls(PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_UNDERFUNDED)

    @classmethod
    def from_path_payment_strict_send_src_no_trust(
        cls,
    ) -> "PathPaymentStrictSendResult":
        return cls(
            PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_SRC_NO_TRUST
        )

    @classmethod
    def from_path_payment_strict_send_src_not_authorized(
        cls,
    ) -> "PathPaymentStrictSendResult":
        return cls(
            PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_SRC_NOT_AUTHORIZED
        )

    @classmethod
    def from_path_payment_strict_send_no_destination(
        cls,
    ) -> "PathPaymentStrictSendResult":
        return cls(
            PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_NO_DESTINATION
        )

    @classmethod
    def from_path_payment_strict_send_no_trust(cls) -> "PathPaymentStrictSendResult":
        return cls(PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_NO_TRUST)

    @classmethod
    def from_path_payment_strict_send_not_authorized(
        cls,
    ) -> "PathPaymentStrictSendResult":
        return cls(
            PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_NOT_AUTHORIZED
        )

    @classmethod
    def from_path_payment_strict_send_line_full(cls) -> "PathPaymentStrictSendResult":
        return cls(PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_LINE_FULL)

    @classmethod
    def from_path_payment_strict_send_no_issuer(
        cls, no_issuer: Asset
    ) -> "PathPaymentStrictSendResult":
        return cls(
            PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_NO_ISSUER,
            no_issuer=no_issuer,
        )

    @classmethod
    def from_path_payment_strict_send_too_few_offers(
        cls,
    ) -> "PathPaymentStrictSendResult":
        return cls(
            PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_TOO_FEW_OFFERS
        )

    @classmethod
    def from_path_payment_strict_send_offer_cross_self(
        cls,
    ) -> "PathPaymentStrictSendResult":
        return cls(
            PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_OFFER_CROSS_SELF
        )

    @classmethod
    def from_path_payment_strict_send_under_destmin(
        cls,
    ) -> "PathPaymentStrictSendResult":
        return cls(
            PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_UNDER_DESTMIN
        )

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

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "PathPaymentStrictSendResult":
        code = PathPaymentStrictSendResultCode.unpack(unpacker)
        if code == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_SUCCESS:
            success = PathPaymentStrictSendResultSuccess.unpack(unpacker)
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
            no_issuer = Asset.unpack(unpacker)
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
        return cls(code=code)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "PathPaymentStrictSendResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "PathPaymentStrictSendResult":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.code == other.code
            and self.success == other.success
            and self.no_issuer == other.no_issuer
        )

    def __str__(self):
        out = []
        out.append(f"code={self.code}")
        out.append(f"success={self.success}") if self.success is not None else None
        out.append(
            f"no_issuer={self.no_issuer}"
        ) if self.no_issuer is not None else None
        return f"<PathPaymentStrictSendResult [{', '.join(out)}]>"
