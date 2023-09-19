# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

__all__ = ["SCErrorCode"]


class SCErrorCode(IntEnum):
    """
    XDR Source Code::

        enum SCErrorCode
        {
            SCEC_ARITH_DOMAIN = 0,      // Some arithmetic was undefined (overflow, divide-by-zero).
            SCEC_INDEX_BOUNDS = 1,      // Something was indexed beyond its bounds.
            SCEC_INVALID_INPUT = 2,     // User provided some otherwise-bad data.
            SCEC_MISSING_VALUE = 3,     // Some value was required but not provided.
            SCEC_EXISTING_VALUE = 4,    // Some value was provided where not allowed.
            SCEC_EXCEEDED_LIMIT = 5,    // Some arbitrary limit -- gas or otherwise -- was hit.
            SCEC_INVALID_ACTION = 6,    // Data was valid but action requested was not.
            SCEC_INTERNAL_ERROR = 7,    // The host detected an error in its own logic.
            SCEC_UNEXPECTED_TYPE = 8,   // Some type wasn't as expected.
            SCEC_UNEXPECTED_SIZE = 9    // Something's size wasn't as expected.
        };
    """

    SCEC_ARITH_DOMAIN = 0
    SCEC_INDEX_BOUNDS = 1
    SCEC_INVALID_INPUT = 2
    SCEC_MISSING_VALUE = 3
    SCEC_EXISTING_VALUE = 4
    SCEC_EXCEEDED_LIMIT = 5
    SCEC_INVALID_ACTION = 6
    SCEC_INTERNAL_ERROR = 7
    SCEC_UNEXPECTED_TYPE = 8
    SCEC_UNEXPECTED_SIZE = 9

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCErrorCode:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCErrorCode:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCErrorCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
