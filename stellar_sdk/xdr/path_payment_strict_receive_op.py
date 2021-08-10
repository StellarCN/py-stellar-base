# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib import Packer, Unpacker

from ..exceptions import ValueError
from .asset import Asset
from .int64 import Int64
from .muxed_account import MuxedAccount

__all__ = ["PathPaymentStrictReceiveOp"]


class PathPaymentStrictReceiveOp:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct PathPaymentStrictReceiveOp
    {
        Asset sendAsset; // asset we pay with
        int64 sendMax;   // the maximum amount of sendAsset to
                         // send (excluding fees).
                         // The operation will fail if can't be met

        MuxedAccount destination; // recipient of the payment
        Asset destAsset;          // what they end up with
        int64 destAmount;         // amount they end up with

        Asset path<5>; // additional hops it must go through to get there
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        send_asset: Asset,
        send_max: Int64,
        destination: MuxedAccount,
        dest_asset: Asset,
        dest_amount: Int64,
        path: List[Asset],
    ) -> None:
        if path and len(path) > 5:
            raise ValueError(
                f"The maximum length of `path` should be 5, but got {len(path)}."
            )
        self.send_asset = send_asset
        self.send_max = send_max
        self.destination = destination
        self.dest_asset = dest_asset
        self.dest_amount = dest_amount
        self.path = path

    def pack(self, packer: Packer) -> None:
        self.send_asset.pack(packer)
        self.send_max.pack(packer)
        self.destination.pack(packer)
        self.dest_asset.pack(packer)
        self.dest_amount.pack(packer)
        packer.pack_uint(len(self.path))
        for path in self.path:
            path.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "PathPaymentStrictReceiveOp":
        send_asset = Asset.unpack(unpacker)
        send_max = Int64.unpack(unpacker)
        destination = MuxedAccount.unpack(unpacker)
        dest_asset = Asset.unpack(unpacker)
        dest_amount = Int64.unpack(unpacker)
        length = unpacker.unpack_uint()
        path = []
        for _ in range(length):
            path.append(Asset.unpack(unpacker))
        return cls(
            send_asset=send_asset,
            send_max=send_max,
            destination=destination,
            dest_asset=dest_asset,
            dest_amount=dest_amount,
            path=path,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "PathPaymentStrictReceiveOp":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "PathPaymentStrictReceiveOp":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.send_asset == other.send_asset
            and self.send_max == other.send_max
            and self.destination == other.destination
            and self.dest_asset == other.dest_asset
            and self.dest_amount == other.dest_amount
            and self.path == other.path
        )

    def __str__(self):
        out = [
            f"send_asset={self.send_asset}",
            f"send_max={self.send_max}",
            f"destination={self.destination}",
            f"dest_asset={self.dest_asset}",
            f"dest_amount={self.dest_amount}",
            f"path={self.path}",
        ]
        return f"<PathPaymentStrictReceiveOp {[', '.join(out)]}>"
