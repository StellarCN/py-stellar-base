# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from enum import IntEnum
from xdrlib import Packer, Unpacker

from ..__version__ import __issues__
from ..exceptions import ValueError

__all__ = ["AccountFlags"]


class AccountFlags(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum AccountFlags
    { // masks for each flag
    
        // Flags set on issuer accounts
        // TrustLines are created with authorized set to "false" requiring
        // the issuer to set it for each TrustLine
        AUTH_REQUIRED_FLAG = 0x1,
        // If set, the authorized flag in TrustLines can be cleared
        // otherwise, authorization cannot be revoked
        AUTH_REVOCABLE_FLAG = 0x2,
        // Once set, causes all AUTH_* flags to be read-only
        AUTH_IMMUTABLE_FLAG = 0x4
    };
    ----------------------------------------------------------------
    """

    AUTH_REQUIRED_FLAG = 1
    AUTH_REVOCABLE_FLAG = 2
    AUTH_IMMUTABLE_FLAG = 4

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AccountFlags":
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "AccountFlags":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AccountFlags":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )
