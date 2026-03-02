# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, Opaque

__all__ = ["AssetCode4"]


class AssetCode4:
    """
    XDR Source Code::

        typedef opaque AssetCode4[4];
    """

    def __init__(self, asset_code4: bytes) -> None:
        _expect_length = 4
        if asset_code4 and len(asset_code4) != _expect_length:
            raise ValueError(
                f"The length of `asset_code4` should be {_expect_length}, but got {len(asset_code4)}."
            )
        self.asset_code4 = asset_code4

    def pack(self, packer: Packer) -> None:
        Opaque(self.asset_code4, 4, True).pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> AssetCode4:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        asset_code4 = Opaque.unpack(unpacker, 4, True)
        return cls(asset_code4)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> AssetCode4:
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
    def from_xdr(cls, xdr: str) -> AssetCode4:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> AssetCode4:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return self.asset_code4.rstrip(b"\x00").decode("ascii")

    @classmethod
    def from_json_dict(cls, json_value: str) -> AssetCode4:
        return cls(json_value.encode("ascii").ljust(4, b"\x00"))

    def __hash__(self):
        return hash((self.asset_code4,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.asset_code4 == other.asset_code4

    def __repr__(self):
        return f"<AssetCode4 [asset_code4={self.asset_code4}]>"
