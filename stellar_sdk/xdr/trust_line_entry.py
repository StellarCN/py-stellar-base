# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .account_id import AccountID
from .int64 import Int64
from .trust_line_asset import TrustLineAsset
from .trust_line_entry_ext import TrustLineEntryExt
from .uint32 import Uint32

__all__ = ["TrustLineEntry"]


class TrustLineEntry:
    """
    XDR Source Code::

        struct TrustLineEntry
        {
            AccountID accountID;  // account this trustline belongs to
            TrustLineAsset asset; // type of asset (with issuer)
            int64 balance;        // how much of this asset the user has.
                                  // Asset defines the unit for this;

            int64 limit;  // balance cannot be above this
            uint32 flags; // see TrustLineFlags

            // reserved for future use
            union switch (int v)
            {
            case 0:
                void;
            case 1:
                struct
                {
                    Liabilities liabilities;

                    union switch (int v)
                    {
                    case 0:
                        void;
                    case 2:
                        TrustLineEntryExtensionV2 v2;
                    }
                    ext;
                } v1;
            }
            ext;
        };
    """

    def __init__(
        self,
        account_id: AccountID,
        asset: TrustLineAsset,
        balance: Int64,
        limit: Int64,
        flags: Uint32,
        ext: TrustLineEntryExt,
    ) -> None:
        self.account_id = account_id
        self.asset = asset
        self.balance = balance
        self.limit = limit
        self.flags = flags
        self.ext = ext

    def pack(self, packer: Packer) -> None:
        self.account_id.pack(packer)
        self.asset.pack(packer)
        self.balance.pack(packer)
        self.limit.pack(packer)
        self.flags.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> TrustLineEntry:
        account_id = AccountID.unpack(unpacker)
        asset = TrustLineAsset.unpack(unpacker)
        balance = Int64.unpack(unpacker)
        limit = Int64.unpack(unpacker)
        flags = Uint32.unpack(unpacker)
        ext = TrustLineEntryExt.unpack(unpacker)
        return cls(
            account_id=account_id,
            asset=asset,
            balance=balance,
            limit=limit,
            flags=flags,
            ext=ext,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TrustLineEntry:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> TrustLineEntry:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.account_id,
                self.asset,
                self.balance,
                self.limit,
                self.flags,
                self.ext,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.account_id == other.account_id
            and self.asset == other.asset
            and self.balance == other.balance
            and self.limit == other.limit
            and self.flags == other.flags
            and self.ext == other.ext
        )

    def __repr__(self):
        out = [
            f"account_id={self.account_id}",
            f"asset={self.asset}",
            f"balance={self.balance}",
            f"limit={self.limit}",
            f"flags={self.flags}",
            f"ext={self.ext}",
        ]
        return f"<TrustLineEntry [{', '.join(out)}]>"
