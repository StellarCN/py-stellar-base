# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

__all__ = ["BinaryFuseFilterType"]


class BinaryFuseFilterType(IntEnum):
    """
    XDR Source Code::

        enum BinaryFuseFilterType
        {
            BINARY_FUSE_FILTER_8_BIT = 0,
            BINARY_FUSE_FILTER_16_BIT = 1,
            BINARY_FUSE_FILTER_32_BIT = 2
        };
    """

    BINARY_FUSE_FILTER_8_BIT = 0
    BINARY_FUSE_FILTER_16_BIT = 1
    BINARY_FUSE_FILTER_32_BIT = 2

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> BinaryFuseFilterType:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> BinaryFuseFilterType:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> BinaryFuseFilterType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
