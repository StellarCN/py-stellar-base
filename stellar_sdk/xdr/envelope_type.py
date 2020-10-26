# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from enum import IntEnum
from xdrlib import Packer, Unpacker

from ..__version__ import __issues__
from ..exceptions import ValueError

__all__ = ["EnvelopeType"]


class EnvelopeType(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum EnvelopeType
    {
        ENVELOPE_TYPE_TX_V0 = 0,
        ENVELOPE_TYPE_SCP = 1,
        ENVELOPE_TYPE_TX = 2,
        ENVELOPE_TYPE_AUTH = 3,
        ENVELOPE_TYPE_SCPVALUE = 4,
        ENVELOPE_TYPE_TX_FEE_BUMP = 5,
        ENVELOPE_TYPE_OP_ID = 6
    };
    ----------------------------------------------------------------
    """

    ENVELOPE_TYPE_TX_V0 = 0
    ENVELOPE_TYPE_SCP = 1
    ENVELOPE_TYPE_TX = 2
    ENVELOPE_TYPE_AUTH = 3
    ENVELOPE_TYPE_SCPVALUE = 4
    ENVELOPE_TYPE_TX_FEE_BUMP = 5
    ENVELOPE_TYPE_OP_ID = 6

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "EnvelopeType":
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "EnvelopeType":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "EnvelopeType":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )
