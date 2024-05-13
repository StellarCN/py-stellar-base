# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

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

            // Number of snapshots to use when calculating average BucketList size
            uint32 bucketListSizeWindowSampleSize;

            // How often to sample the BucketList size for the average, in ledgers
            uint32 bucketListWindowSamplePeriod;

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
        bucket_list_size_window_sample_size: Uint32,
        bucket_list_window_sample_period: Uint32,
        eviction_scan_size: Uint32,
        starting_eviction_scan_level: Uint32,
    ) -> None:
        self.max_entry_ttl = max_entry_ttl
        self.min_temporary_ttl = min_temporary_ttl
        self.min_persistent_ttl = min_persistent_ttl
        self.persistent_rent_rate_denominator = persistent_rent_rate_denominator
        self.temp_rent_rate_denominator = temp_rent_rate_denominator
        self.max_entries_to_archive = max_entries_to_archive
        self.bucket_list_size_window_sample_size = bucket_list_size_window_sample_size
        self.bucket_list_window_sample_period = bucket_list_window_sample_period
        self.eviction_scan_size = eviction_scan_size
        self.starting_eviction_scan_level = starting_eviction_scan_level

    def pack(self, packer: Packer) -> None:
        self.max_entry_ttl.pack(packer)
        self.min_temporary_ttl.pack(packer)
        self.min_persistent_ttl.pack(packer)
        self.persistent_rent_rate_denominator.pack(packer)
        self.temp_rent_rate_denominator.pack(packer)
        self.max_entries_to_archive.pack(packer)
        self.bucket_list_size_window_sample_size.pack(packer)
        self.bucket_list_window_sample_period.pack(packer)
        self.eviction_scan_size.pack(packer)
        self.starting_eviction_scan_level.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> StateArchivalSettings:
        max_entry_ttl = Uint32.unpack(unpacker)
        min_temporary_ttl = Uint32.unpack(unpacker)
        min_persistent_ttl = Uint32.unpack(unpacker)
        persistent_rent_rate_denominator = Int64.unpack(unpacker)
        temp_rent_rate_denominator = Int64.unpack(unpacker)
        max_entries_to_archive = Uint32.unpack(unpacker)
        bucket_list_size_window_sample_size = Uint32.unpack(unpacker)
        bucket_list_window_sample_period = Uint32.unpack(unpacker)
        eviction_scan_size = Uint32.unpack(unpacker)
        starting_eviction_scan_level = Uint32.unpack(unpacker)
        return cls(
            max_entry_ttl=max_entry_ttl,
            min_temporary_ttl=min_temporary_ttl,
            min_persistent_ttl=min_persistent_ttl,
            persistent_rent_rate_denominator=persistent_rent_rate_denominator,
            temp_rent_rate_denominator=temp_rent_rate_denominator,
            max_entries_to_archive=max_entries_to_archive,
            bucket_list_size_window_sample_size=bucket_list_size_window_sample_size,
            bucket_list_window_sample_period=bucket_list_window_sample_period,
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
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> StateArchivalSettings:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.max_entry_ttl,
                self.min_temporary_ttl,
                self.min_persistent_ttl,
                self.persistent_rent_rate_denominator,
                self.temp_rent_rate_denominator,
                self.max_entries_to_archive,
                self.bucket_list_size_window_sample_size,
                self.bucket_list_window_sample_period,
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
            and self.bucket_list_size_window_sample_size
            == other.bucket_list_size_window_sample_size
            and self.bucket_list_window_sample_period
            == other.bucket_list_window_sample_period
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
            f"bucket_list_size_window_sample_size={self.bucket_list_size_window_sample_size}",
            f"bucket_list_window_sample_period={self.bucket_list_window_sample_period}",
            f"eviction_scan_size={self.eviction_scan_size}",
            f"starting_eviction_scan_level={self.starting_eviction_scan_level}",
        ]
        return f"<StateArchivalSettings [{', '.join(out)}]>"
