# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .base import Opaque

__all__ = ["AssetCode4"]


class AssetCode4:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef opaque AssetCode4[4];
    ----------------------------------------------------------------
    """

    def __init__(self, asset_code4: bytes) -> None:
        self.asset_code4 = asset_code4

    def pack(self, packer: Packer) -> None:
        Opaque(self.asset_code4, 4, True).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AssetCode4":
        asset_code4 = Opaque.unpack(unpacker, 4, True)
        return cls(asset_code4)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "AssetCode4":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AssetCode4":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.asset_code4 == other.asset_code4

    def __str__(self):
        return f"<AssetCode4 [asset_code4={self.asset_code4}]>"
