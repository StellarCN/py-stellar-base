# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from enum import IntEnum
from xdrlib import Packer, Unpacker

from ..__version__ import __issues__
from ..exceptions import ValueError

__all__ = ["OperationResultCode"]


class OperationResultCode(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum OperationResultCode
    {
        opINNER = 0, // inner object result is valid

        opBAD_AUTH = -1,            // too few valid signatures / wrong network
        opNO_ACCOUNT = -2,          // source account was not found
        opNOT_SUPPORTED = -3,       // operation not supported at this time
        opTOO_MANY_SUBENTRIES = -4, // max number of subentries already reached
        opEXCEEDED_WORK_LIMIT = -5, // operation did too much work
        opTOO_MANY_SPONSORING = -6  // account is sponsoring too many entries
    };
    ----------------------------------------------------------------
    """

    opINNER = 0
    opBAD_AUTH = -1
    opNO_ACCOUNT = -2
    opNOT_SUPPORTED = -3
    opTOO_MANY_SUBENTRIES = -4
    opEXCEEDED_WORK_LIMIT = -5
    opTOO_MANY_SPONSORING = -6

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "OperationResultCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "OperationResultCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "OperationResultCode":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )
