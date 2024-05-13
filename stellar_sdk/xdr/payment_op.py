# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .asset import Asset
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
    def unpack(cls, unpacker: Unpacker) -> PaymentOp:
        destination = MuxedAccount.unpack(unpacker)
        asset = Asset.unpack(unpacker)
        amount = Int64.unpack(unpacker)
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
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> PaymentOp:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
