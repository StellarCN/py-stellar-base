# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .account_id import AccountID
from .asset_code4 import AssetCode4

__all__ = ["AssetAlphaNum4"]


class AssetAlphaNum4:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct
        {
            AssetCode4 assetCode;
            AccountID issuer;
        }
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        asset_code: AssetCode4,
        issuer: AccountID,
    ) -> None:
        self.asset_code = asset_code
        self.issuer = issuer

    def pack(self, packer: Packer) -> None:
        self.asset_code.pack(packer)
        self.issuer.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AssetAlphaNum4":
        asset_code = AssetCode4.unpack(unpacker)
        issuer = AccountID.unpack(unpacker)
        return cls(
            asset_code=asset_code,
            issuer=issuer,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "AssetAlphaNum4":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AssetAlphaNum4":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.asset_code == other.asset_code and self.issuer == other.issuer

    def __str__(self):
        out = [
            f"asset_code={self.asset_code}",
            f"issuer={self.issuer}",
        ]
        return f"<AssetAlphaNum4 {[', '.join(out)]}>"
