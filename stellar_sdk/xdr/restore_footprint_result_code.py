# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

__all__ = ["RestoreFootprintResultCode"]


class RestoreFootprintResultCode(IntEnum):
    """
    XDR Source Code::

        enum RestoreFootprintResultCode
        {
            // codes considered as "success" for the operation
            RESTORE_FOOTPRINT_SUCCESS = 0,

            // codes considered as "failure" for the operation
            RESTORE_FOOTPRINT_MALFORMED = -1,
            RESTORE_FOOTPRINT_RESOURCE_LIMIT_EXCEEDED = -2,
            RESTORE_FOOTPRINT_INSUFFICIENT_REFUNDABLE_FEE = -3
        };
    """

    RESTORE_FOOTPRINT_SUCCESS = 0
    RESTORE_FOOTPRINT_MALFORMED = -1
    RESTORE_FOOTPRINT_RESOURCE_LIMIT_EXCEEDED = -2
    RESTORE_FOOTPRINT_INSUFFICIENT_REFUNDABLE_FEE = -3

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> RestoreFootprintResultCode:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> RestoreFootprintResultCode:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> RestoreFootprintResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
