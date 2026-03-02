# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> StellarValue:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        tx_set_hash = Hash.unpack(unpacker, depth_limit - 1)
        close_time = TimePoint.unpack(unpacker, depth_limit - 1)
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"upgrades length {length} exceeds remaining input length {_remaining}"
            )
        upgrades = []
        for _ in range(length):
            upgrades.append(UpgradeType.unpack(unpacker, depth_limit - 1))
        ext = StellarValueExt.unpack(unpacker, depth_limit - 1)
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> StellarValue:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> StellarValue:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "tx_set_hash": self.tx_set_hash.to_json_dict(),
            "close_time": self.close_time.to_json_dict(),
            "upgrades": [item.to_json_dict() for item in self.upgrades],
            "ext": self.ext.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> StellarValue:
        tx_set_hash = Hash.from_json_dict(json_dict["tx_set_hash"])
        close_time = TimePoint.from_json_dict(json_dict["close_time"])
        upgrades = [UpgradeType.from_json_dict(item) for item in json_dict["upgrades"]]
        ext = StellarValueExt.from_json_dict(json_dict["ext"])
        return cls(
            tx_set_hash=tx_set_hash,
            close_time=close_time,
            upgrades=upgrades,
            ext=ext,
        )

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
