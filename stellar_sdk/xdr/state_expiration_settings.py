# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .int64 import Int64
from .uint32 import Uint32
from .uint64 import Uint64

__all__ = ["StateExpirationSettings"]


class StateExpirationSettings:
    """
    XDR Source Code::

        struct StateExpirationSettings {
            uint32 maxEntryExpiration;
            uint32 minTempEntryExpiration;
            uint32 minPersistentEntryExpiration;

            // rent_fee = wfee_rate_average / rent_rate_denominator_for_type
            int64 persistentRentRateDenominator;
            int64 tempRentRateDenominator;

            // max number of entries that emit expiration meta in a single ledger
            uint32 maxEntriesToExpire;

            // Number of snapshots to use when calculating average BucketList size
            uint32 bucketListSizeWindowSampleSize;

            // Maximum number of bytes that we scan for eviction per ledger
            uint64 evictionScanSize;

            // Lowest BucketList level to be scanned to evict entries
            uint32 startingEvictionScanLevel;
        };
    """

    def __init__(
        self,
        max_entry_expiration: Uint32,
        min_temp_entry_expiration: Uint32,
        min_persistent_entry_expiration: Uint32,
        persistent_rent_rate_denominator: Int64,
        temp_rent_rate_denominator: Int64,
        max_entries_to_expire: Uint32,
        bucket_list_size_window_sample_size: Uint32,
        eviction_scan_size: Uint64,
        starting_eviction_scan_level: Uint32,
    ) -> None:
        self.max_entry_expiration = max_entry_expiration
        self.min_temp_entry_expiration = min_temp_entry_expiration
        self.min_persistent_entry_expiration = min_persistent_entry_expiration
        self.persistent_rent_rate_denominator = persistent_rent_rate_denominator
        self.temp_rent_rate_denominator = temp_rent_rate_denominator
        self.max_entries_to_expire = max_entries_to_expire
        self.bucket_list_size_window_sample_size = bucket_list_size_window_sample_size
        self.eviction_scan_size = eviction_scan_size
        self.starting_eviction_scan_level = starting_eviction_scan_level

    def pack(self, packer: Packer) -> None:
        self.max_entry_expiration.pack(packer)
        self.min_temp_entry_expiration.pack(packer)
        self.min_persistent_entry_expiration.pack(packer)
        self.persistent_rent_rate_denominator.pack(packer)
        self.temp_rent_rate_denominator.pack(packer)
        self.max_entries_to_expire.pack(packer)
        self.bucket_list_size_window_sample_size.pack(packer)
        self.eviction_scan_size.pack(packer)
        self.starting_eviction_scan_level.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> StateExpirationSettings:
        max_entry_expiration = Uint32.unpack(unpacker)
        min_temp_entry_expiration = Uint32.unpack(unpacker)
        min_persistent_entry_expiration = Uint32.unpack(unpacker)
        persistent_rent_rate_denominator = Int64.unpack(unpacker)
        temp_rent_rate_denominator = Int64.unpack(unpacker)
        max_entries_to_expire = Uint32.unpack(unpacker)
        bucket_list_size_window_sample_size = Uint32.unpack(unpacker)
        eviction_scan_size = Uint64.unpack(unpacker)
        starting_eviction_scan_level = Uint32.unpack(unpacker)
        return cls(
            max_entry_expiration=max_entry_expiration,
            min_temp_entry_expiration=min_temp_entry_expiration,
            min_persistent_entry_expiration=min_persistent_entry_expiration,
            persistent_rent_rate_denominator=persistent_rent_rate_denominator,
            temp_rent_rate_denominator=temp_rent_rate_denominator,
            max_entries_to_expire=max_entries_to_expire,
            bucket_list_size_window_sample_size=bucket_list_size_window_sample_size,
            eviction_scan_size=eviction_scan_size,
            starting_eviction_scan_level=starting_eviction_scan_level,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> StateExpirationSettings:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> StateExpirationSettings:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.max_entry_expiration,
                self.min_temp_entry_expiration,
                self.min_persistent_entry_expiration,
                self.persistent_rent_rate_denominator,
                self.temp_rent_rate_denominator,
                self.max_entries_to_expire,
                self.bucket_list_size_window_sample_size,
                self.eviction_scan_size,
                self.starting_eviction_scan_level,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.max_entry_expiration == other.max_entry_expiration
            and self.min_temp_entry_expiration == other.min_temp_entry_expiration
            and self.min_persistent_entry_expiration
            == other.min_persistent_entry_expiration
            and self.persistent_rent_rate_denominator
            == other.persistent_rent_rate_denominator
            and self.temp_rent_rate_denominator == other.temp_rent_rate_denominator
            and self.max_entries_to_expire == other.max_entries_to_expire
            and self.bucket_list_size_window_sample_size
            == other.bucket_list_size_window_sample_size
            and self.eviction_scan_size == other.eviction_scan_size
            and self.starting_eviction_scan_level == other.starting_eviction_scan_level
        )

    def __str__(self):
        out = [
            f"max_entry_expiration={self.max_entry_expiration}",
            f"min_temp_entry_expiration={self.min_temp_entry_expiration}",
            f"min_persistent_entry_expiration={self.min_persistent_entry_expiration}",
            f"persistent_rent_rate_denominator={self.persistent_rent_rate_denominator}",
            f"temp_rent_rate_denominator={self.temp_rent_rate_denominator}",
            f"max_entries_to_expire={self.max_entries_to_expire}",
            f"bucket_list_size_window_sample_size={self.bucket_list_size_window_sample_size}",
            f"eviction_scan_size={self.eviction_scan_size}",
            f"starting_eviction_scan_level={self.starting_eviction_scan_level}",
        ]
        return f"<StateExpirationSettings [{', '.join(out)}]>"
