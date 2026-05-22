# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .int64 import Int64
from .uint32 import Uint32

__all__ = ["StateArchivalSettings"]


class StateArchivalSettings:
    """
    XDR Source Code::

        struct StateArchivalSettings {
            uint32 maxEntryTTL;
            uint32 minTemporaryTTL;
            uint32 minPersistentTTL;

            // rent_fee = wfee_rate_average / rent_rate_denominator_for_type
            int64 persistentRentRateDenominator;
            int64 tempRentRateDenominator;

            // max number of entries that emit archival meta in a single ledger
            uint32 maxEntriesToArchive;

            // Number of snapshots to use when calculating average live Soroban State size
            uint32 liveSorobanStateSizeWindowSampleSize;

            // How often to sample the live Soroban State size for the average, in ledgers
            uint32 liveSorobanStateSizeWindowSamplePeriod;

            // Maximum number of bytes that we scan for eviction per ledger
            uint32 evictionScanSize;

            // Lowest BucketList level to be scanned to evict entries
            uint32 startingEvictionScanLevel;
        };
    """

    def __init__(
        self,
        max_entry_ttl: Uint32,
        min_temporary_ttl: Uint32,
        min_persistent_ttl: Uint32,
        persistent_rent_rate_denominator: Int64,
        temp_rent_rate_denominator: Int64,
        max_entries_to_archive: Uint32,
        live_soroban_state_size_window_sample_size: Uint32,
        live_soroban_state_size_window_sample_period: Uint32,
        eviction_scan_size: Uint32,
        starting_eviction_scan_level: Uint32,
    ) -> None:
        self.max_entry_ttl = max_entry_ttl
        self.min_temporary_ttl = min_temporary_ttl
        self.min_persistent_ttl = min_persistent_ttl
        self.persistent_rent_rate_denominator = persistent_rent_rate_denominator
        self.temp_rent_rate_denominator = temp_rent_rate_denominator
        self.max_entries_to_archive = max_entries_to_archive
        self.live_soroban_state_size_window_sample_size = (
            live_soroban_state_size_window_sample_size
        )
        self.live_soroban_state_size_window_sample_period = (
            live_soroban_state_size_window_sample_period
        )
        self.eviction_scan_size = eviction_scan_size
        self.starting_eviction_scan_level = starting_eviction_scan_level

    def pack(self, packer: Packer) -> None:
        self.max_entry_ttl.pack(packer)
        self.min_temporary_ttl.pack(packer)
        self.min_persistent_ttl.pack(packer)
        self.persistent_rent_rate_denominator.pack(packer)
        self.temp_rent_rate_denominator.pack(packer)
        self.max_entries_to_archive.pack(packer)
        self.live_soroban_state_size_window_sample_size.pack(packer)
        self.live_soroban_state_size_window_sample_period.pack(packer)
        self.eviction_scan_size.pack(packer)
        self.starting_eviction_scan_level.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> StateArchivalSettings:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        max_entry_ttl = Uint32.unpack(unpacker, depth_limit - 1)
        min_temporary_ttl = Uint32.unpack(unpacker, depth_limit - 1)
        min_persistent_ttl = Uint32.unpack(unpacker, depth_limit - 1)
        persistent_rent_rate_denominator = Int64.unpack(unpacker, depth_limit - 1)
        temp_rent_rate_denominator = Int64.unpack(unpacker, depth_limit - 1)
        max_entries_to_archive = Uint32.unpack(unpacker, depth_limit - 1)
        live_soroban_state_size_window_sample_size = Uint32.unpack(
            unpacker, depth_limit - 1
        )
        live_soroban_state_size_window_sample_period = Uint32.unpack(
            unpacker, depth_limit - 1
        )
        eviction_scan_size = Uint32.unpack(unpacker, depth_limit - 1)
        starting_eviction_scan_level = Uint32.unpack(unpacker, depth_limit - 1)
        return cls(
            max_entry_ttl=max_entry_ttl,
            min_temporary_ttl=min_temporary_ttl,
            min_persistent_ttl=min_persistent_ttl,
            persistent_rent_rate_denominator=persistent_rent_rate_denominator,
            temp_rent_rate_denominator=temp_rent_rate_denominator,
            max_entries_to_archive=max_entries_to_archive,
            live_soroban_state_size_window_sample_size=live_soroban_state_size_window_sample_size,
            live_soroban_state_size_window_sample_period=live_soroban_state_size_window_sample_period,
            eviction_scan_size=eviction_scan_size,
            starting_eviction_scan_level=starting_eviction_scan_level,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> StateArchivalSettings:
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
    def from_xdr(cls, xdr: str) -> StateArchivalSettings:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> StateArchivalSettings:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "max_entry_ttl": self.max_entry_ttl.to_json_dict(),
            "min_temporary_ttl": self.min_temporary_ttl.to_json_dict(),
            "min_persistent_ttl": self.min_persistent_ttl.to_json_dict(),
            "persistent_rent_rate_denominator": self.persistent_rent_rate_denominator.to_json_dict(),
            "temp_rent_rate_denominator": self.temp_rent_rate_denominator.to_json_dict(),
            "max_entries_to_archive": self.max_entries_to_archive.to_json_dict(),
            "live_soroban_state_size_window_sample_size": self.live_soroban_state_size_window_sample_size.to_json_dict(),
            "live_soroban_state_size_window_sample_period": self.live_soroban_state_size_window_sample_period.to_json_dict(),
            "eviction_scan_size": self.eviction_scan_size.to_json_dict(),
            "starting_eviction_scan_level": self.starting_eviction_scan_level.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> StateArchivalSettings:
        max_entry_ttl = Uint32.from_json_dict(json_dict["max_entry_ttl"])
        min_temporary_ttl = Uint32.from_json_dict(json_dict["min_temporary_ttl"])
        min_persistent_ttl = Uint32.from_json_dict(json_dict["min_persistent_ttl"])
        persistent_rent_rate_denominator = Int64.from_json_dict(
            json_dict["persistent_rent_rate_denominator"]
        )
        temp_rent_rate_denominator = Int64.from_json_dict(
            json_dict["temp_rent_rate_denominator"]
        )
        max_entries_to_archive = Uint32.from_json_dict(
            json_dict["max_entries_to_archive"]
        )
        live_soroban_state_size_window_sample_size = Uint32.from_json_dict(
            json_dict["live_soroban_state_size_window_sample_size"]
        )
        live_soroban_state_size_window_sample_period = Uint32.from_json_dict(
            json_dict["live_soroban_state_size_window_sample_period"]
        )
        eviction_scan_size = Uint32.from_json_dict(json_dict["eviction_scan_size"])
        starting_eviction_scan_level = Uint32.from_json_dict(
            json_dict["starting_eviction_scan_level"]
        )
        return cls(
            max_entry_ttl=max_entry_ttl,
            min_temporary_ttl=min_temporary_ttl,
            min_persistent_ttl=min_persistent_ttl,
            persistent_rent_rate_denominator=persistent_rent_rate_denominator,
            temp_rent_rate_denominator=temp_rent_rate_denominator,
            max_entries_to_archive=max_entries_to_archive,
            live_soroban_state_size_window_sample_size=live_soroban_state_size_window_sample_size,
            live_soroban_state_size_window_sample_period=live_soroban_state_size_window_sample_period,
            eviction_scan_size=eviction_scan_size,
            starting_eviction_scan_level=starting_eviction_scan_level,
        )

    def __hash__(self):
        return hash(
            (
                self.max_entry_ttl,
                self.min_temporary_ttl,
                self.min_persistent_ttl,
                self.persistent_rent_rate_denominator,
                self.temp_rent_rate_denominator,
                self.max_entries_to_archive,
                self.live_soroban_state_size_window_sample_size,
                self.live_soroban_state_size_window_sample_period,
                self.eviction_scan_size,
                self.starting_eviction_scan_level,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.max_entry_ttl == other.max_entry_ttl
            and self.min_temporary_ttl == other.min_temporary_ttl
            and self.min_persistent_ttl == other.min_persistent_ttl
            and self.persistent_rent_rate_denominator
            == other.persistent_rent_rate_denominator
            and self.temp_rent_rate_denominator == other.temp_rent_rate_denominator
            and self.max_entries_to_archive == other.max_entries_to_archive
            and self.live_soroban_state_size_window_sample_size
            == other.live_soroban_state_size_window_sample_size
            and self.live_soroban_state_size_window_sample_period
            == other.live_soroban_state_size_window_sample_period
            and self.eviction_scan_size == other.eviction_scan_size
            and self.starting_eviction_scan_level == other.starting_eviction_scan_level
        )

    def __repr__(self):
        out = [
            f"max_entry_ttl={self.max_entry_ttl}",
            f"min_temporary_ttl={self.min_temporary_ttl}",
            f"min_persistent_ttl={self.min_persistent_ttl}",
            f"persistent_rent_rate_denominator={self.persistent_rent_rate_denominator}",
            f"temp_rent_rate_denominator={self.temp_rent_rate_denominator}",
            f"max_entries_to_archive={self.max_entries_to_archive}",
            f"live_soroban_state_size_window_sample_size={self.live_soroban_state_size_window_sample_size}",
            f"live_soroban_state_size_window_sample_period={self.live_soroban_state_size_window_sample_period}",
            f"eviction_scan_size={self.eviction_scan_size}",
            f"starting_eviction_scan_level={self.starting_eviction_scan_level}",
        ]
        return f"<StateArchivalSettings [{', '.join(out)}]>"
