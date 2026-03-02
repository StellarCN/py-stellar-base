# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, Opaque

__all__ = ["AssetCode12"]


class AssetCode12:
    """
    XDR Source Code::

        typedef opaque AssetCode12[12];
    """

    def __init__(self, asset_code12: bytes) -> None:
        _expect_length = 12
        if asset_code12 and len(asset_code12) != _expect_length:
            raise ValueError(
                f"The length of `asset_code12` should be {_expect_length}, but got {len(asset_code12)}."
            )
        self.asset_code12 = asset_code12

    def pack(self, packer: Packer) -> None:
        Opaque(self.asset_code12, 12, True).pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> AssetCode12:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        asset_code12 = Opaque.unpack(unpacker, 12, True)
        return cls(asset_code12)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> AssetCode12:
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
    def from_xdr(cls, xdr: str) -> AssetCode12:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> AssetCode12:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        trimmed = self.asset_code12.rstrip(b"\x00")
        return self.asset_code12[: max(len(trimmed), 5)].decode("ascii")

    @classmethod
    def from_json_dict(cls, json_value: str) -> AssetCode12:
        return cls(json_value.encode("ascii").ljust(12, b"\x00"))

    def __hash__(self):
        return hash((self.asset_code12,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.asset_code12 == other.asset_code12

    def __repr__(self):
        return f"<AssetCode12 [asset_code12={self.asset_code12}]>"
