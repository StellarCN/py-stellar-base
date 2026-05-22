# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .account_id import AccountID
from .base import DEFAULT_XDR_MAX_DEPTH
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> TrustLineEntry:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        account_id = AccountID.unpack(unpacker, depth_limit - 1)
        asset = TrustLineAsset.unpack(unpacker, depth_limit - 1)
        balance = Int64.unpack(unpacker, depth_limit - 1)
        limit = Int64.unpack(unpacker, depth_limit - 1)
        flags = Uint32.unpack(unpacker, depth_limit - 1)
        ext = TrustLineEntryExt.unpack(unpacker, depth_limit - 1)
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> TrustLineEntry:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TrustLineEntry:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "account_id": self.account_id.to_json_dict(),
            "asset": self.asset.to_json_dict(),
            "balance": self.balance.to_json_dict(),
            "limit": self.limit.to_json_dict(),
            "flags": self.flags.to_json_dict(),
            "ext": self.ext.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> TrustLineEntry:
        account_id = AccountID.from_json_dict(json_dict["account_id"])
        asset = TrustLineAsset.from_json_dict(json_dict["asset"])
        balance = Int64.from_json_dict(json_dict["balance"])
        limit = Int64.from_json_dict(json_dict["limit"])
        flags = Uint32.from_json_dict(json_dict["flags"])
        ext = TrustLineEntryExt.from_json_dict(json_dict["ext"])
        return cls(
            account_id=account_id,
            asset=asset,
            balance=balance,
            limit=limit,
            flags=flags,
            ext=ext,
        )

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
