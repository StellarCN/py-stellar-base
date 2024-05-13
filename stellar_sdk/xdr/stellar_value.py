# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

from .hash import Hash
from .stellar_value_ext import StellarValueExt
from .time_point import TimePoint
from .upgrade_type import UpgradeType

__all__ = ["StellarValue"]


class StellarValue:
    """
    XDR Source Code::

        struct StellarValue
        {
            Hash txSetHash;      // transaction set to apply to previous ledger
            TimePoint closeTime; // network close time

            // upgrades to apply to the previous ledger (usually empty)
            // this is a vector of encoded 'LedgerUpgrade' so that nodes can drop
            // unknown steps during consensus if needed.
            // see notes below on 'LedgerUpgrade' for more detail
            // max size is dictated by number of upgrade types (+ room for future)
            UpgradeType upgrades<6>;

            // reserved for future use
            union switch (StellarValueType v)
            {
            case STELLAR_VALUE_BASIC:
                void;
            case STELLAR_VALUE_SIGNED:
                LedgerCloseValueSignature lcValueSignature;
            }
            ext;
        };
    """

    def __init__(
        self,
        tx_set_hash: Hash,
        close_time: TimePoint,
        upgrades: List[UpgradeType],
        ext: StellarValueExt,
    ) -> None:
        _expect_max_length = 6
        if upgrades and len(upgrades) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `upgrades` should be {_expect_max_length}, but got {len(upgrades)}."
            )
        self.tx_set_hash = tx_set_hash
        self.close_time = close_time
        self.upgrades = upgrades
        self.ext = ext

    def pack(self, packer: Packer) -> None:
        self.tx_set_hash.pack(packer)
        self.close_time.pack(packer)
        packer.pack_uint(len(self.upgrades))
        for upgrades_item in self.upgrades:
            upgrades_item.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> StellarValue:
        tx_set_hash = Hash.unpack(unpacker)
        close_time = TimePoint.unpack(unpacker)
        length = unpacker.unpack_uint()
        upgrades = []
        for _ in range(length):
            upgrades.append(UpgradeType.unpack(unpacker))
        ext = StellarValueExt.unpack(unpacker)
        return cls(
            tx_set_hash=tx_set_hash,
            close_time=close_time,
            upgrades=upgrades,
            ext=ext,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> StellarValue:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> StellarValue:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.tx_set_hash,
                self.close_time,
                self.upgrades,
                self.ext,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.tx_set_hash == other.tx_set_hash
            and self.close_time == other.close_time
            and self.upgrades == other.upgrades
            and self.ext == other.ext
        )

    def __repr__(self):
        out = [
            f"tx_set_hash={self.tx_set_hash}",
            f"close_time={self.close_time}",
            f"upgrades={self.upgrades}",
            f"ext={self.ext}",
        ]
        return f"<StellarValue [{', '.join(out)}]>"
