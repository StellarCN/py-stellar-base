# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .account_id import AccountID
from .asset_code import AssetCode
from .uint32 import Uint32

__all__ = ["AllowTrustOp"]


class AllowTrustOp:
    """
    XDR Source Code::

        struct AllowTrustOp
        {
            AccountID trustor;
            AssetCode asset;

            // One of 0, AUTHORIZED_FLAG, or AUTHORIZED_TO_MAINTAIN_LIABILITIES_FLAG
            uint32 authorize;
        };
    """

    def __init__(
        self,
        trustor: AccountID,
        asset: AssetCode,
        authorize: Uint32,
    ) -> None:
        self.trustor = trustor
        self.asset = asset
        self.authorize = authorize

    def pack(self, packer: Packer) -> None:
        self.trustor.pack(packer)
        self.asset.pack(packer)
        self.authorize.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> AllowTrustOp:
        trustor = AccountID.unpack(unpacker)
        asset = AssetCode.unpack(unpacker)
        authorize = Uint32.unpack(unpacker)
        return cls(
            trustor=trustor,
            asset=asset,
            authorize=authorize,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> AllowTrustOp:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> AllowTrustOp:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.trustor,
                self.asset,
                self.authorize,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.trustor == other.trustor
            and self.asset == other.asset
            and self.authorize == other.authorize
        )

    def __repr__(self):
        out = [
            f"trustor={self.trustor}",
            f"asset={self.asset}",
            f"authorize={self.authorize}",
        ]
        return f"<AllowTrustOp [{', '.join(out)}]>"
