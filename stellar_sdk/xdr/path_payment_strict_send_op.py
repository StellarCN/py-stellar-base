# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib import Packer, Unpacker

from .asset import Asset
from .int64 import Int64
from .muxed_account import MuxedAccount
from ..exceptions import ValueError

__all__ = ["PathPaymentStrictSendOp"]


class PathPaymentStrictSendOp:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct PathPaymentStrictSendOp
    {
        Asset sendAsset;  // asset we pay with
        int64 sendAmount; // amount of sendAsset to send (excluding fees)
    
        MuxedAccount destination; // recipient of the payment
        Asset destAsset;          // what they end up with
        int64 destMin;            // the minimum amount of dest asset to
                                  // be received
                                  // The operation will fail if it can't be met
    
        Asset path<5>; // additional hops it must go through to get there
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        send_asset: Asset,
        send_amount: Int64,
        destination: MuxedAccount,
        dest_asset: Asset,
        dest_min: Int64,
        path: List[Asset],
    ) -> None:
        if path and len(path) > 5:
            raise ValueError(
                f"The maximum length of `path` should be 5, but got {len(path)}."
            )
        self.send_asset = send_asset
        self.send_amount = send_amount
        self.destination = destination
        self.dest_asset = dest_asset
        self.dest_min = dest_min
        self.path = path

    def pack(self, packer: Packer) -> None:
        self.send_asset.pack(packer)
        self.send_amount.pack(packer)
        self.destination.pack(packer)
        self.dest_asset.pack(packer)
        self.dest_min.pack(packer)
        packer.pack_uint(len(self.path))
        for path in self.path:
            path.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "PathPaymentStrictSendOp":
        send_asset = Asset.unpack(unpacker)
        send_amount = Int64.unpack(unpacker)
        destination = MuxedAccount.unpack(unpacker)
        dest_asset = Asset.unpack(unpacker)
        dest_min = Int64.unpack(unpacker)
        length = unpacker.unpack_uint()
        path = []
        for _ in range(length):
            path.append(Asset.unpack(unpacker))
        return cls(
            send_asset=send_asset,
            send_amount=send_amount,
            destination=destination,
            dest_asset=dest_asset,
            dest_min=dest_min,
            path=path,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "PathPaymentStrictSendOp":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "PathPaymentStrictSendOp":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.send_asset == other.send_asset
            and self.send_amount == other.send_amount
            and self.destination == other.destination
            and self.dest_asset == other.dest_asset
            and self.dest_min == other.dest_min
            and self.path == other.path
        )

    def __str__(self):
        out = [
            f"send_asset={self.send_asset}",
            f"send_amount={self.send_amount}",
            f"destination={self.destination}",
            f"dest_asset={self.dest_asset}",
            f"dest_min={self.dest_min}",
            f"path={self.path}",
        ]
        return f"<PathPaymentStrictSendOp {[', '.join(out)]}>"
