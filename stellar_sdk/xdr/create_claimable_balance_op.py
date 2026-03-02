# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .asset import Asset
from .base import DEFAULT_XDR_MAX_DEPTH
from .claimant import Claimant
from .int64 import Int64

__all__ = ["CreateClaimableBalanceOp"]


class CreateClaimableBalanceOp:
    """
    XDR Source Code::

        struct CreateClaimableBalanceOp
        {
            Asset asset;
            int64 amount;
            Claimant claimants<10>;
        };
    """

    def __init__(
        self,
        asset: Asset,
        amount: Int64,
        claimants: List[Claimant],
    ) -> None:
        _expect_max_length = 10
        if claimants and len(claimants) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `claimants` should be {_expect_max_length}, but got {len(claimants)}."
            )
        self.asset = asset
        self.amount = amount
        self.claimants = claimants

    def pack(self, packer: Packer) -> None:
        self.asset.pack(packer)
        self.amount.pack(packer)
        packer.pack_uint(len(self.claimants))
        for claimants_item in self.claimants:
            claimants_item.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> CreateClaimableBalanceOp:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        asset = Asset.unpack(unpacker, depth_limit - 1)
        amount = Int64.unpack(unpacker, depth_limit - 1)
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"claimants length {length} exceeds remaining input length {_remaining}"
            )
        claimants = []
        for _ in range(length):
            claimants.append(Claimant.unpack(unpacker, depth_limit - 1))
        return cls(
            asset=asset,
            amount=amount,
            claimants=claimants,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> CreateClaimableBalanceOp:
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
    def from_xdr(cls, xdr: str) -> CreateClaimableBalanceOp:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> CreateClaimableBalanceOp:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "asset": self.asset.to_json_dict(),
            "amount": self.amount.to_json_dict(),
            "claimants": [item.to_json_dict() for item in self.claimants],
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> CreateClaimableBalanceOp:
        asset = Asset.from_json_dict(json_dict["asset"])
        amount = Int64.from_json_dict(json_dict["amount"])
        claimants = [Claimant.from_json_dict(item) for item in json_dict["claimants"]]
        return cls(
            asset=asset,
            amount=amount,
            claimants=claimants,
        )

    def __hash__(self):
        return hash(
            (
                self.asset,
                self.amount,
                self.claimants,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.asset == other.asset
            and self.amount == other.amount
            and self.claimants == other.claimants
        )

    def __repr__(self):
        out = [
            f"asset={self.asset}",
            f"amount={self.amount}",
            f"claimants={self.claimants}",
        ]
        return f"<CreateClaimableBalanceOp [{', '.join(out)}]>"
