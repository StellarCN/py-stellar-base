# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

__all__ = ["BumpFootprintExpirationResultCode"]


class BumpFootprintExpirationResultCode(IntEnum):
    """
    XDR Source Code::

        enum BumpFootprintExpirationResultCode
        {
            // codes considered as "success" for the operation
            BUMP_FOOTPRINT_EXPIRATION_SUCCESS = 0,

            // codes considered as "failure" for the operation
            BUMP_FOOTPRINT_EXPIRATION_MALFORMED = -1,
            BUMP_FOOTPRINT_EXPIRATION_RESOURCE_LIMIT_EXCEEDED = -2
        };
    """

    BUMP_FOOTPRINT_EXPIRATION_SUCCESS = 0
    BUMP_FOOTPRINT_EXPIRATION_MALFORMED = -1
    BUMP_FOOTPRINT_EXPIRATION_RESOURCE_LIMIT_EXCEEDED = -2

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> BumpFootprintExpirationResultCode:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> BumpFootprintExpirationResultCode:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> BumpFootprintExpirationResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
