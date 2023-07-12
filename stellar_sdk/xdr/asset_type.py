# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

__all__ = ["AssetType"]


class AssetType(IntEnum):
    """
    XDR Source Code::

        enum AssetType
        {
            ASSET_TYPE_NATIVE = 0,
            ASSET_TYPE_CREDIT_ALPHANUM4 = 1,
            ASSET_TYPE_CREDIT_ALPHANUM12 = 2,
            ASSET_TYPE_POOL_SHARE = 3
        };
    """

    ASSET_TYPE_NATIVE = 0
    ASSET_TYPE_CREDIT_ALPHANUM4 = 1
    ASSET_TYPE_CREDIT_ALPHANUM12 = 2
    ASSET_TYPE_POOL_SHARE = 3

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> AssetType:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> AssetType:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> AssetType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
