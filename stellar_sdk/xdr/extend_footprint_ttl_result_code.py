# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

__all__ = ["ExtendFootprintTTLResultCode"]


class ExtendFootprintTTLResultCode(IntEnum):
    """
    XDR Source Code::

        enum ExtendFootprintTTLResultCode
        {
            // codes considered as "success" for the operation
            EXTEND_FOOTPRINT_TTL_SUCCESS = 0,

            // codes considered as "failure" for the operation
            EXTEND_FOOTPRINT_TTL_MALFORMED = -1,
            EXTEND_FOOTPRINT_TTL_RESOURCE_LIMIT_EXCEEDED = -2,
            EXTEND_FOOTPRINT_TTL_INSUFFICIENT_REFUNDABLE_FEE = -3
        };
    """

    EXTEND_FOOTPRINT_TTL_SUCCESS = 0
    EXTEND_FOOTPRINT_TTL_MALFORMED = -1
    EXTEND_FOOTPRINT_TTL_RESOURCE_LIMIT_EXCEEDED = -2
    EXTEND_FOOTPRINT_TTL_INSUFFICIENT_REFUNDABLE_FEE = -3

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ExtendFootprintTTLResultCode:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ExtendFootprintTTLResultCode:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ExtendFootprintTTLResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
