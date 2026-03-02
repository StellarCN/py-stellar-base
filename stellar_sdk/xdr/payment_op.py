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

__all__ = ["PaymentOp"]


class PaymentOp:
    """
    XDR Source Code::

        struct PaymentOp
        {
            MuxedAccount destination; // recipient of the payment
            Asset asset;              // what they end up with
            int64 amount;             // amount they end up with
        };
    """

    def __init__(
        self,
        destination: MuxedAccount,
        asset: Asset,
        amount: Int64,
    ) -> None:
        self.destination = destination
        self.asset = asset
        self.amount = amount

    def pack(self, packer: Packer) -> None:
        self.destination.pack(packer)
        self.asset.pack(packer)
        self.amount.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> PaymentOp:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        destination = MuxedAccount.unpack(unpacker, depth_limit - 1)
        asset = Asset.unpack(unpacker, depth_limit - 1)
        amount = Int64.unpack(unpacker, depth_limit - 1)
        return cls(
            destination=destination,
            asset=asset,
            amount=amount,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> PaymentOp:
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
    def from_xdr(cls, xdr: str) -> PaymentOp:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> PaymentOp:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "destination": self.destination.to_json_dict(),
            "asset": self.asset.to_json_dict(),
            "amount": self.amount.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> PaymentOp:
        destination = MuxedAccount.from_json_dict(json_dict["destination"])
        asset = Asset.from_json_dict(json_dict["asset"])
        amount = Int64.from_json_dict(json_dict["amount"])
        return cls(
            destination=destination,
            asset=asset,
            amount=amount,
        )

    def __hash__(self):
        return hash(
            (
                self.destination,
                self.asset,
                self.amount,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.destination == other.destination
            and self.asset == other.asset
            and self.amount == other.amount
        )

    def __repr__(self):
        out = [
            f"destination={self.destination}",
            f"asset={self.asset}",
            f"amount={self.amount}",
        ]
        return f"<PaymentOp [{', '.join(out)}]>"
