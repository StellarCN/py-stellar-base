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

__all__ = ["PathPaymentStrictReceiveOp"]


class PathPaymentStrictReceiveOp:
    """
    XDR Source Code::

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
        _expect_max_length = 5
        if path and len(path) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `path` should be {_expect_max_length}, but got {len(path)}."
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
        for path_item in self.path:
            path_item.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> PathPaymentStrictReceiveOp:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        send_asset = Asset.unpack(unpacker, depth_limit - 1)
        send_max = Int64.unpack(unpacker, depth_limit - 1)
        destination = MuxedAccount.unpack(unpacker, depth_limit - 1)
        dest_asset = Asset.unpack(unpacker, depth_limit - 1)
        dest_amount = Int64.unpack(unpacker, depth_limit - 1)
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
    def from_xdr_bytes(cls, xdr: bytes) -> PathPaymentStrictReceiveOp:
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
    def from_xdr(cls, xdr: str) -> PathPaymentStrictReceiveOp:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> PathPaymentStrictReceiveOp:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "send_asset": self.send_asset.to_json_dict(),
            "send_max": self.send_max.to_json_dict(),
            "destination": self.destination.to_json_dict(),
            "dest_asset": self.dest_asset.to_json_dict(),
            "dest_amount": self.dest_amount.to_json_dict(),
            "path": [item.to_json_dict() for item in self.path],
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> PathPaymentStrictReceiveOp:
        send_asset = Asset.from_json_dict(json_dict["send_asset"])
        send_max = Int64.from_json_dict(json_dict["send_max"])
        destination = MuxedAccount.from_json_dict(json_dict["destination"])
        dest_asset = Asset.from_json_dict(json_dict["dest_asset"])
        dest_amount = Int64.from_json_dict(json_dict["dest_amount"])
        path = [Asset.from_json_dict(item) for item in json_dict["path"]]
        return cls(
            send_asset=send_asset,
            send_max=send_max,
            destination=destination,
            dest_asset=dest_asset,
            dest_amount=dest_amount,
            path=path,
        )

    def __hash__(self):
        return hash(
            (
                self.send_asset,
                self.send_max,
                self.destination,
                self.dest_asset,
                self.dest_amount,
                self.path,
            )
        )

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

    def __repr__(self):
        out = [
            f"send_asset={self.send_asset}",
            f"send_max={self.send_max}",
            f"destination={self.destination}",
            f"dest_asset={self.dest_asset}",
            f"dest_amount={self.dest_amount}",
            f"path={self.path}",
        ]
        return f"<PathPaymentStrictReceiveOp [{', '.join(out)}]>"
