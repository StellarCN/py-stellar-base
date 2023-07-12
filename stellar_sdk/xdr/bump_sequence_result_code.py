# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

__all__ = ["BumpSequenceResultCode"]


class BumpSequenceResultCode(IntEnum):
    """
    XDR Source Code::

        enum BumpSequenceResultCode
        {
            // codes considered as "success" for the operation
            BUMP_SEQUENCE_SUCCESS = 0,
            // codes considered as "failure" for the operation
            BUMP_SEQUENCE_BAD_SEQ = -1 // `bumpTo` is not within bounds
        };
    """

    BUMP_SEQUENCE_SUCCESS = 0
    BUMP_SEQUENCE_BAD_SEQ = -1

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> BumpSequenceResultCode:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> BumpSequenceResultCode:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> BumpSequenceResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
