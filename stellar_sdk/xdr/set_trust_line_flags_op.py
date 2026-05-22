# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .account_id import AccountID
from .asset import Asset
from .base import DEFAULT_XDR_MAX_DEPTH
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SetTrustLineFlagsOp:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        trustor = AccountID.unpack(unpacker, depth_limit - 1)
        asset = Asset.unpack(unpacker, depth_limit - 1)
        clear_flags = Uint32.unpack(unpacker, depth_limit - 1)
        set_flags = Uint32.unpack(unpacker, depth_limit - 1)
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SetTrustLineFlagsOp:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SetTrustLineFlagsOp:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "trustor": self.trustor.to_json_dict(),
            "asset": self.asset.to_json_dict(),
            "clear_flags": self.clear_flags.to_json_dict(),
            "set_flags": self.set_flags.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SetTrustLineFlagsOp:
        trustor = AccountID.from_json_dict(json_dict["trustor"])
        asset = Asset.from_json_dict(json_dict["asset"])
        clear_flags = Uint32.from_json_dict(json_dict["clear_flags"])
        set_flags = Uint32.from_json_dict(json_dict["set_flags"])
        return cls(
            trustor=trustor,
            asset=asset,
            clear_flags=clear_flags,
            set_flags=set_flags,
        )

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
