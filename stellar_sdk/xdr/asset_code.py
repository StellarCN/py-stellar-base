# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .asset_code4 import AssetCode4
from .asset_code12 import AssetCode12
from .asset_type import AssetType

__all__ = ["AssetCode"]


class AssetCode:
    """
    XDR Source Code::

        union AssetCode switch (AssetType type)
        {
        case ASSET_TYPE_CREDIT_ALPHANUM4:
            AssetCode4 assetCode4;

        case ASSET_TYPE_CREDIT_ALPHANUM12:
            AssetCode12 assetCode12;

            // add other asset types here in the future
        };
    """

    def __init__(
        self,
        type: AssetType,
        asset_code4: AssetCode4 = None,
        asset_code12: AssetCode12 = None,
    ) -> None:
        self.type = type
        self.asset_code4 = asset_code4
        self.asset_code12 = asset_code12

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM4:
            if self.asset_code4 is None:
                raise ValueError("asset_code4 should not be None.")
            self.asset_code4.pack(packer)
            return
        if self.type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM12:
            if self.asset_code12 is None:
                raise ValueError("asset_code12 should not be None.")
            self.asset_code12.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> AssetCode:
        type = AssetType.unpack(unpacker)
        if type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM4:
            asset_code4 = AssetCode4.unpack(unpacker)
            return cls(type=type, asset_code4=asset_code4)
        if type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM12:
            asset_code12 = AssetCode12.unpack(unpacker)
            return cls(type=type, asset_code12=asset_code12)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> AssetCode:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> AssetCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.type,
                self.asset_code4,
                self.asset_code12,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.asset_code4 == other.asset_code4
            and self.asset_code12 == other.asset_code12
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        (
            out.append(f"asset_code4={self.asset_code4}")
            if self.asset_code4 is not None
            else None
        )
        (
            out.append(f"asset_code12={self.asset_code12}")
            if self.asset_code12 is not None
            else None
        )
        return f"<AssetCode [{', '.join(out)}]>"
