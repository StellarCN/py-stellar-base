# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .base import Opaque

__all__ = ["AssetCode12"]


class AssetCode12:
    """
    XDR Source Code::

        typedef opaque AssetCode12[12];
    """

    def __init__(self, asset_code12: bytes) -> None:
        self.asset_code12 = asset_code12

    def pack(self, packer: Packer) -> None:
        Opaque(self.asset_code12, 12, True).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> AssetCode12:
        asset_code12 = Opaque.unpack(unpacker, 12, True)
        return cls(asset_code12)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> AssetCode12:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> AssetCode12:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(self.asset_code12)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.asset_code12 == other.asset_code12

    def __repr__(self):
        return f"<AssetCode12 [asset_code12={self.asset_code12}]>"
