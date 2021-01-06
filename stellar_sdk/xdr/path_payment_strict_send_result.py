# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .asset import Asset
from .path_payment_strict_send_result_code import PathPaymentStrictSendResultCode
from .path_payment_strict_send_result_success import PathPaymentStrictSendResultSuccess
from ..exceptions import ValueError

__all__ = ["PathPaymentStrictSendResult"]


class PathPaymentStrictSendResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union PathPaymentStrictSendResult switch (PathPaymentStrictSendResultCode code)
    {
    case PATH_PAYMENT_STRICT_SEND_SUCCESS:
        struct
        {
            ClaimOfferAtom offers<>;
            SimplePaymentResult last;
        } success;
    case PATH_PAYMENT_STRICT_SEND_NO_ISSUER:
        Asset noIssuer; // the asset that caused the error
    default:
        void;
    };
    ----------------------------------------------------------------
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
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_NO_ISSUER
        ):
            if self.no_issuer is None:
                raise ValueError("no_issuer should not be None.")
            self.no_issuer.pack(packer)
            return
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "PathPaymentStrictSendResult":
        code = PathPaymentStrictSendResultCode.unpack(unpacker)
        if code == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_SUCCESS:
            success = PathPaymentStrictSendResultSuccess.unpack(unpacker)
            if success is None:
                raise ValueError("success should not be None.")
            return cls(code, success=success)
        if code == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_NO_ISSUER:
            no_issuer = Asset.unpack(unpacker)
            if no_issuer is None:
                raise ValueError("no_issuer should not be None.")
            return cls(code, no_issuer=no_issuer)
        raise ValueError("Invalid code.")

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
        return f"<PathPaymentStrictSendResult {[', '.join(out)]}>"
