# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .asset_alpha_num12 import AssetAlphaNum12
from .asset_alpha_num4 import AssetAlphaNum4
from .asset_type import AssetType
from ..exceptions import ValueError

__all__ = ["Asset"]


class Asset:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union Asset switch (AssetType type)
    {
    case ASSET_TYPE_NATIVE: // Not credit
        void;
    
    case ASSET_TYPE_CREDIT_ALPHANUM4:
        struct
        {
            AssetCode4 assetCode;
            AccountID issuer;
        } alphaNum4;
    
    case ASSET_TYPE_CREDIT_ALPHANUM12:
        struct
        {
            AssetCode12 assetCode;
            AccountID issuer;
        } alphaNum12;
    
        // add other asset types here in the future
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: AssetType,
        alpha_num4: AssetAlphaNum4 = None,
        alpha_num12: AssetAlphaNum12 = None,
    ) -> None:
        self.type = type
        self.alpha_num4 = alpha_num4
        self.alpha_num12 = alpha_num12

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == AssetType.ASSET_TYPE_NATIVE:
            return
        if self.type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM4:
            if self.alpha_num4 is None:
                raise ValueError("alpha_num4 should not be None.")
            self.alpha_num4.pack(packer)
            return
        if self.type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM12:
            if self.alpha_num12 is None:
                raise ValueError("alpha_num12 should not be None.")
            self.alpha_num12.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Asset":
        type = AssetType.unpack(unpacker)
        if type == AssetType.ASSET_TYPE_NATIVE:
            return cls(type)
        if type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM4:
            alpha_num4 = AssetAlphaNum4.unpack(unpacker)
            if alpha_num4 is None:
                raise ValueError("alpha_num4 should not be None.")
            return cls(type, alpha_num4=alpha_num4)
        if type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM12:
            alpha_num12 = AssetAlphaNum12.unpack(unpacker)
            if alpha_num12 is None:
                raise ValueError("alpha_num12 should not be None.")
            return cls(type, alpha_num12=alpha_num12)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "Asset":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Asset":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.alpha_num4 == other.alpha_num4
            and self.alpha_num12 == other.alpha_num12
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(
            f"alpha_num4={self.alpha_num4}"
        ) if self.alpha_num4 is not None else None
        out.append(
            f"alpha_num12={self.alpha_num12}"
        ) if self.alpha_num12 is not None else None
        return f"<Asset {[', '.join(out)]}>"
