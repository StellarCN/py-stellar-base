# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from enum import IntEnum
from xdrlib import Packer, Unpacker

from ..__version__ import __issues__
from ..exceptions import ValueError

__all__ = ["ManageDataResultCode"]


class ManageDataResultCode(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum ManageDataResultCode
    {
        // codes considered as "success" for the operation
        MANAGE_DATA_SUCCESS = 0,
        // codes considered as "failure" for the operation
        MANAGE_DATA_NOT_SUPPORTED_YET =
            -1, // The network hasn't moved to this protocol change yet
        MANAGE_DATA_NAME_NOT_FOUND =
            -2, // Trying to remove a Data Entry that isn't there
        MANAGE_DATA_LOW_RESERVE = -3, // not enough funds to create a new Data Entry
        MANAGE_DATA_INVALID_NAME = -4 // Name not a valid string
    };
    ----------------------------------------------------------------
    """

    MANAGE_DATA_SUCCESS = 0
    MANAGE_DATA_NOT_SUPPORTED_YET = -1
    MANAGE_DATA_NAME_NOT_FOUND = -2
    MANAGE_DATA_LOW_RESERVE = -3
    MANAGE_DATA_INVALID_NAME = -4

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ManageDataResultCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "ManageDataResultCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ManageDataResultCode":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )
