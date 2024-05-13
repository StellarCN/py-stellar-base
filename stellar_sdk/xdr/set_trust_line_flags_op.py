# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .account_id import AccountID
from .asset import Asset
from .uint32 import Uint32

__all__ = ["SetTrustLineFlagsOp"]


class SetTrustLineFlagsOp:
    """
    XDR Source Code::

        struct SetTrustLineFlagsOp
        {
            AccountID trustor;
            Asset asset;

            uint32 clearFlags; // which flags to clear
            uint32 setFlags;   // which flags to set
        };
    """

    def __init__(
        self,
        trustor: AccountID,
        asset: Asset,
        clear_flags: Uint32,
        set_flags: Uint32,
    ) -> None:
        self.trustor = trustor
        self.asset = asset
        self.clear_flags = clear_flags
        self.set_flags = set_flags

    def pack(self, packer: Packer) -> None:
        self.trustor.pack(packer)
        self.asset.pack(packer)
        self.clear_flags.pack(packer)
        self.set_flags.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SetTrustLineFlagsOp:
        trustor = AccountID.unpack(unpacker)
        asset = Asset.unpack(unpacker)
        clear_flags = Uint32.unpack(unpacker)
        set_flags = Uint32.unpack(unpacker)
        return cls(
            trustor=trustor,
            asset=asset,
            clear_flags=clear_flags,
            set_flags=set_flags,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SetTrustLineFlagsOp:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SetTrustLineFlagsOp:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.trustor,
                self.asset,
                self.clear_flags,
                self.set_flags,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.trustor == other.trustor
            and self.asset == other.asset
            and self.clear_flags == other.clear_flags
            and self.set_flags == other.set_flags
        )

    def __repr__(self):
        out = [
            f"trustor={self.trustor}",
            f"asset={self.asset}",
            f"clear_flags={self.clear_flags}",
            f"set_flags={self.set_flags}",
        ]
        return f"<SetTrustLineFlagsOp [{', '.join(out)}]>"
