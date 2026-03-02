# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .asset import Asset
from .base import DEFAULT_XDR_MAX_DEPTH
from .int64 import Int64
from .muxed_account import MuxedAccount

__all__ = ["ClawbackOp"]


class ClawbackOp:
    """
    XDR Source Code::

        struct ClawbackOp
        {
            Asset asset;
            MuxedAccount from_;
            int64 amount;
        };
    """

    def __init__(
        self,
        asset: Asset,
        from_: MuxedAccount,
        amount: Int64,
    ) -> None:
        self.asset = asset
        self.from_ = from_
        self.amount = amount

    def pack(self, packer: Packer) -> None:
        self.asset.pack(packer)
        self.from_.pack(packer)
        self.amount.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ClawbackOp:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        asset = Asset.unpack(unpacker, depth_limit - 1)
        from_ = MuxedAccount.unpack(unpacker, depth_limit - 1)
        amount = Int64.unpack(unpacker, depth_limit - 1)
        return cls(
            asset=asset,
            from_=from_,
            amount=amount,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ClawbackOp:
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
    def from_xdr(cls, xdr: str) -> ClawbackOp:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ClawbackOp:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "asset": self.asset.to_json_dict(),
            "from_": self.from_.to_json_dict(),
            "amount": self.amount.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> ClawbackOp:
        asset = Asset.from_json_dict(json_dict["asset"])
        from_ = MuxedAccount.from_json_dict(json_dict["from_"])
        amount = Int64.from_json_dict(json_dict["amount"])
        return cls(
            asset=asset,
            from_=from_,
            amount=amount,
        )

    def __hash__(self):
        return hash(
            (
                self.asset,
                self.from_,
                self.amount,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.asset == other.asset
            and self.from_ == other.from_
            and self.amount == other.amount
        )

    def __repr__(self):
        out = [
            f"asset={self.asset}",
            f"from_={self.from_}",
            f"amount={self.amount}",
        ]
        return f"<ClawbackOp [{', '.join(out)}]>"
