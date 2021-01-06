# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from enum import IntEnum
from xdrlib import Packer, Unpacker

from ..__version__ import __issues__
from ..exceptions import ValueError

__all__ = ["PaymentResultCode"]


class PaymentResultCode(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum PaymentResultCode
    {
        // codes considered as "success" for the operation
        PAYMENT_SUCCESS = 0, // payment successfuly completed
    
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
    ----------------------------------------------------------------
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
    def unpack(cls, unpacker: Unpacker) -> "PaymentResultCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "PaymentResultCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "PaymentResultCode":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )
