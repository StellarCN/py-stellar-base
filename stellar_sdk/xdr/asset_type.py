# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_ASSET_TYPE_MAP = {
    0: "native",
    1: "credit_alphanum4",
    2: "credit_alphanum12",
    3: "pool_share",
}
_ASSET_TYPE_REVERSE_MAP = {
    "native": 0,
    "credit_alphanum4": 1,
    "credit_alphanum12": 2,
    "pool_share": 3,
}
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> AssetType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> AssetType:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _ASSET_TYPE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> AssetType:
        return cls(_ASSET_TYPE_REVERSE_MAP[json_value])
