# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from enum import IntEnum
from xdrlib import Packer, Unpacker

from ..__version__ import __issues__
from ..exceptions import ValueError

__all__ = ["SetTrustLineFlagsResultCode"]


class SetTrustLineFlagsResultCode(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum SetTrustLineFlagsResultCode
    {
        // codes considered as "success" for the operation
        SET_TRUST_LINE_FLAGS_SUCCESS = 0,

        // codes considered as "failure" for the operation
        SET_TRUST_LINE_FLAGS_MALFORMED = -1,
        SET_TRUST_LINE_FLAGS_NO_TRUST_LINE = -2,
        SET_TRUST_LINE_FLAGS_CANT_REVOKE = -3,
        SET_TRUST_LINE_FLAGS_INVALID_STATE = -4
    };
    ----------------------------------------------------------------
    """

    SET_TRUST_LINE_FLAGS_SUCCESS = 0
    SET_TRUST_LINE_FLAGS_MALFORMED = -1
    SET_TRUST_LINE_FLAGS_NO_TRUST_LINE = -2
    SET_TRUST_LINE_FLAGS_CANT_REVOKE = -3
    SET_TRUST_LINE_FLAGS_INVALID_STATE = -4

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SetTrustLineFlagsResultCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SetTrustLineFlagsResultCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SetTrustLineFlagsResultCode":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )
