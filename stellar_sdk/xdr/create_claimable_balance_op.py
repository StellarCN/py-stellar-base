# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

from .asset import Asset
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
    def unpack(cls, unpacker: Unpacker) -> CreateClaimableBalanceOp:
        asset = Asset.unpack(unpacker)
        amount = Int64.unpack(unpacker)
        length = unpacker.unpack_uint()
        claimants = []
        for _ in range(length):
            claimants.append(Claimant.unpack(unpacker))
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
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> CreateClaimableBalanceOp:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
