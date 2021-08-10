# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from ..exceptions import ValueError
from .manage_offer_success_result import ManageOfferSuccessResult
from .manage_sell_offer_result_code import ManageSellOfferResultCode

__all__ = ["ManageSellOfferResult"]


class ManageSellOfferResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union ManageSellOfferResult switch (ManageSellOfferResultCode code)
    {
    case MANAGE_SELL_OFFER_SUCCESS:
        ManageOfferSuccessResult success;
    default:
        void;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        code: ManageSellOfferResultCode,
        success: ManageOfferSuccessResult = None,
    ) -> None:
        self.code = code
        self.success = success

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == ManageSellOfferResultCode.MANAGE_SELL_OFFER_SUCCESS:
            if self.success is None:
                raise ValueError("success should not be None.")
            self.success.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ManageSellOfferResult":
        code = ManageSellOfferResultCode.unpack(unpacker)
        if code == ManageSellOfferResultCode.MANAGE_SELL_OFFER_SUCCESS:
            success = ManageOfferSuccessResult.unpack(unpacker)
            if success is None:
                raise ValueError("success should not be None.")
            return cls(code, success=success)
        return cls(code)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "ManageSellOfferResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ManageSellOfferResult":
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
        return f"<ManageSellOfferResult {[', '.join(out)]}>"
