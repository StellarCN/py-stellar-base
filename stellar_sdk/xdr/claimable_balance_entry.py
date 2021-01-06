# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib import Packer, Unpacker

from .asset import Asset
from .claimable_balance_entry_ext import ClaimableBalanceEntryExt
from .claimable_balance_id import ClaimableBalanceID
from .claimant import Claimant
from .int64 import Int64
from ..exceptions import ValueError

__all__ = ["ClaimableBalanceEntry"]


class ClaimableBalanceEntry:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct ClaimableBalanceEntry
    {
        // Unique identifier for this ClaimableBalanceEntry
        ClaimableBalanceID balanceID;
    
        // List of claimants with associated predicate
        Claimant claimants<10>;
    
        // Any asset including native
        Asset asset;
    
        // Amount of asset
        int64 amount;
    
        // reserved for future use
        union switch (int v)
        {
        case 0:
            void;
        }
        ext;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        balance_id: ClaimableBalanceID,
        claimants: List[Claimant],
        asset: Asset,
        amount: Int64,
        ext: ClaimableBalanceEntryExt,
    ) -> None:
        if claimants and len(claimants) > 10:
            raise ValueError(
                f"The maximum length of `claimants` should be 10, but got {len(claimants)}."
            )
        self.balance_id = balance_id
        self.claimants = claimants
        self.asset = asset
        self.amount = amount
        self.ext = ext

    def pack(self, packer: Packer) -> None:
        self.balance_id.pack(packer)
        packer.pack_uint(len(self.claimants))
        for claimant in self.claimants:
            claimant.pack(packer)
        self.asset.pack(packer)
        self.amount.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ClaimableBalanceEntry":
        balance_id = ClaimableBalanceID.unpack(unpacker)
        length = unpacker.unpack_uint()
        claimants = []
        for _ in range(length):
            claimants.append(Claimant.unpack(unpacker))
        asset = Asset.unpack(unpacker)
        amount = Int64.unpack(unpacker)
        ext = ClaimableBalanceEntryExt.unpack(unpacker)
        return cls(
            balance_id=balance_id,
            claimants=claimants,
            asset=asset,
            amount=amount,
            ext=ext,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "ClaimableBalanceEntry":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ClaimableBalanceEntry":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.balance_id == other.balance_id
            and self.claimants == other.claimants
            and self.asset == other.asset
            and self.amount == other.amount
            and self.ext == other.ext
        )

    def __str__(self):
        out = [
            f"balance_id={self.balance_id}",
            f"claimants={self.claimants}",
            f"asset={self.asset}",
            f"amount={self.amount}",
            f"ext={self.ext}",
        ]
        return f"<ClaimableBalanceEntry {[', '.join(out)]}>"
