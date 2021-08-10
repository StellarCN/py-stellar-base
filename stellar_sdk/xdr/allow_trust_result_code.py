# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from enum import IntEnum
from xdrlib import Packer, Unpacker

from ..__version__ import __issues__
from ..exceptions import ValueError

__all__ = ["AllowTrustResultCode"]


class AllowTrustResultCode(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum AllowTrustResultCode
    {
        // codes considered as "success" for the operation
        ALLOW_TRUST_SUCCESS = 0,
        // codes considered as "failure" for the operation
        ALLOW_TRUST_MALFORMED = -1,     // asset is not ASSET_TYPE_ALPHANUM
        ALLOW_TRUST_NO_TRUST_LINE = -2, // trustor does not have a trustline
                                        // source account does not require trust
        ALLOW_TRUST_TRUST_NOT_REQUIRED = -3,
        ALLOW_TRUST_CANT_REVOKE = -4,     // source account can't revoke trust,
        ALLOW_TRUST_SELF_NOT_ALLOWED = -5 // trusting self is not allowed
    };
    ----------------------------------------------------------------
    """

    ALLOW_TRUST_SUCCESS = 0
    ALLOW_TRUST_MALFORMED = -1
    ALLOW_TRUST_NO_TRUST_LINE = -2
    ALLOW_TRUST_TRUST_NOT_REQUIRED = -3
    ALLOW_TRUST_CANT_REVOKE = -4
    ALLOW_TRUST_SELF_NOT_ALLOWED = -5

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AllowTrustResultCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "AllowTrustResultCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AllowTrustResultCode":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )
