# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .asset import Asset
from .base import DEFAULT_XDR_MAX_DEPTH
from .int64 import Int64
from .muxed_account import MuxedAccount

__all__ = ["PathPaymentStrictSendOp"]


class PathPaymentStrictSendOp:
    """
    XDR Source Code::

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
        _expect_max_length = 5
        if path and len(path) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `path` should be {_expect_max_length}, but got {len(path)}."
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
        for path_item in self.path:
            path_item.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> PathPaymentStrictSendOp:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        send_asset = Asset.unpack(unpacker, depth_limit - 1)
        send_amount = Int64.unpack(unpacker, depth_limit - 1)
        destination = MuxedAccount.unpack(unpacker, depth_limit - 1)
        dest_asset = Asset.unpack(unpacker, depth_limit - 1)
        dest_min = Int64.unpack(unpacker, depth_limit - 1)
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"path length {length} exceeds remaining input length {_remaining}"
            )
        path = []
        for _ in range(length):
            path.append(Asset.unpack(unpacker, depth_limit - 1))
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
    def from_xdr_bytes(cls, xdr: bytes) -> PathPaymentStrictSendOp:
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
    def from_xdr(cls, xdr: str) -> PathPaymentStrictSendOp:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> PathPaymentStrictSendOp:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "send_asset": self.send_asset.to_json_dict(),
            "send_amount": self.send_amount.to_json_dict(),
            "destination": self.destination.to_json_dict(),
            "dest_asset": self.dest_asset.to_json_dict(),
            "dest_min": self.dest_min.to_json_dict(),
            "path": [item.to_json_dict() for item in self.path],
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> PathPaymentStrictSendOp:
        send_asset = Asset.from_json_dict(json_dict["send_asset"])
        send_amount = Int64.from_json_dict(json_dict["send_amount"])
        destination = MuxedAccount.from_json_dict(json_dict["destination"])
        dest_asset = Asset.from_json_dict(json_dict["dest_asset"])
        dest_min = Int64.from_json_dict(json_dict["dest_min"])
        path = [Asset.from_json_dict(item) for item in json_dict["path"]]
        return cls(
            send_asset=send_asset,
            send_amount=send_amount,
            destination=destination,
            dest_asset=dest_asset,
            dest_min=dest_min,
            path=path,
        )

    def __hash__(self):
        return hash(
            (
                self.send_asset,
                self.send_amount,
                self.destination,
                self.dest_asset,
                self.dest_min,
                self.path,
            )
        )

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

    def __repr__(self):
        out = [
            f"send_asset={self.send_asset}",
            f"send_amount={self.send_amount}",
            f"destination={self.destination}",
            f"dest_asset={self.dest_asset}",
            f"dest_min={self.dest_min}",
            f"path={self.path}",
        ]
        return f"<PathPaymentStrictSendOp [{', '.join(out)}]>"
