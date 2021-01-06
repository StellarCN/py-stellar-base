# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from enum import IntEnum
from xdrlib import Packer, Unpacker

from ..__version__ import __issues__
from ..exceptions import ValueError

__all__ = ["PathPaymentStrictReceiveResultCode"]


class PathPaymentStrictReceiveResultCode(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum PathPaymentStrictReceiveResultCode
    {
        // codes considered as "success" for the operation
        PATH_PAYMENT_STRICT_RECEIVE_SUCCESS = 0, // success
    
        // codes considered as "failure" for the operation
        PATH_PAYMENT_STRICT_RECEIVE_MALFORMED = -1, // bad input
        PATH_PAYMENT_STRICT_RECEIVE_UNDERFUNDED =
            -2, // not enough funds in source account
        PATH_PAYMENT_STRICT_RECEIVE_SRC_NO_TRUST =
            -3, // no trust line on source account
        PATH_PAYMENT_STRICT_RECEIVE_SRC_NOT_AUTHORIZED =
            -4, // source not authorized to transfer
        PATH_PAYMENT_STRICT_RECEIVE_NO_DESTINATION =
            -5, // destination account does not exist
        PATH_PAYMENT_STRICT_RECEIVE_NO_TRUST =
            -6, // dest missing a trust line for asset
        PATH_PAYMENT_STRICT_RECEIVE_NOT_AUTHORIZED =
            -7, // dest not authorized to hold asset
        PATH_PAYMENT_STRICT_RECEIVE_LINE_FULL =
            -8, // dest would go above their limit
        PATH_PAYMENT_STRICT_RECEIVE_NO_ISSUER = -9, // missing issuer on one asset
        PATH_PAYMENT_STRICT_RECEIVE_TOO_FEW_OFFERS =
            -10, // not enough offers to satisfy path
        PATH_PAYMENT_STRICT_RECEIVE_OFFER_CROSS_SELF =
            -11, // would cross one of its own offers
        PATH_PAYMENT_STRICT_RECEIVE_OVER_SENDMAX = -12 // could not satisfy sendmax
    };
    ----------------------------------------------------------------
    """

    PATH_PAYMENT_STRICT_RECEIVE_SUCCESS = 0
    PATH_PAYMENT_STRICT_RECEIVE_MALFORMED = -1
    PATH_PAYMENT_STRICT_RECEIVE_UNDERFUNDED = -2
    PATH_PAYMENT_STRICT_RECEIVE_SRC_NO_TRUST = -3
    PATH_PAYMENT_STRICT_RECEIVE_SRC_NOT_AUTHORIZED = -4
    PATH_PAYMENT_STRICT_RECEIVE_NO_DESTINATION = -5
    PATH_PAYMENT_STRICT_RECEIVE_NO_TRUST = -6
    PATH_PAYMENT_STRICT_RECEIVE_NOT_AUTHORIZED = -7
    PATH_PAYMENT_STRICT_RECEIVE_LINE_FULL = -8
    PATH_PAYMENT_STRICT_RECEIVE_NO_ISSUER = -9
    PATH_PAYMENT_STRICT_RECEIVE_TOO_FEW_OFFERS = -10
    PATH_PAYMENT_STRICT_RECEIVE_OFFER_CROSS_SELF = -11
    PATH_PAYMENT_STRICT_RECEIVE_OVER_SENDMAX = -12

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "PathPaymentStrictReceiveResultCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "PathPaymentStrictReceiveResultCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "PathPaymentStrictReceiveResultCode":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )
