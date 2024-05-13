# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .int64 import Int64
from .uint32 import Uint32

__all__ = ["ConfigSettingContractLedgerCostV0"]


class ConfigSettingContractLedgerCostV0:
    """
    XDR Source Code::

        struct ConfigSettingContractLedgerCostV0
        {
            // Maximum number of ledger entry read operations per ledger
            uint32 ledgerMaxReadLedgerEntries;
            // Maximum number of bytes that can be read per ledger
            uint32 ledgerMaxReadBytes;
            // Maximum number of ledger entry write operations per ledger
            uint32 ledgerMaxWriteLedgerEntries;
            // Maximum number of bytes that can be written per ledger
            uint32 ledgerMaxWriteBytes;

            // Maximum number of ledger entry read operations per transaction
            uint32 txMaxReadLedgerEntries;
            // Maximum number of bytes that can be read per transaction
            uint32 txMaxReadBytes;
            // Maximum number of ledger entry write operations per transaction
            uint32 txMaxWriteLedgerEntries;
            // Maximum number of bytes that can be written per transaction
            uint32 txMaxWriteBytes;

            int64 feeReadLedgerEntry;  // Fee per ledger entry read
            int64 feeWriteLedgerEntry; // Fee per ledger entry write

            int64 feeRead1KB;  // Fee for reading 1KB

            // The following parameters determine the write fee per 1KB.
            // Write fee grows linearly until bucket list reaches this size
            int64 bucketListTargetSizeBytes;
            // Fee per 1KB write when the bucket list is empty
            int64 writeFee1KBBucketListLow;
            // Fee per 1KB write when the bucket list has reached `bucketListTargetSizeBytes`
            int64 writeFee1KBBucketListHigh;
            // Write fee multiplier for any additional data past the first `bucketListTargetSizeBytes`
            uint32 bucketListWriteFeeGrowthFactor;
        };
    """

    def __init__(
        self,
        ledger_max_read_ledger_entries: Uint32,
        ledger_max_read_bytes: Uint32,
        ledger_max_write_ledger_entries: Uint32,
        ledger_max_write_bytes: Uint32,
        tx_max_read_ledger_entries: Uint32,
        tx_max_read_bytes: Uint32,
        tx_max_write_ledger_entries: Uint32,
        tx_max_write_bytes: Uint32,
        fee_read_ledger_entry: Int64,
        fee_write_ledger_entry: Int64,
        fee_read1_kb: Int64,
        bucket_list_target_size_bytes: Int64,
        write_fee1_kb_bucket_list_low: Int64,
        write_fee1_kb_bucket_list_high: Int64,
        bucket_list_write_fee_growth_factor: Uint32,
    ) -> None:
        self.ledger_max_read_ledger_entries = ledger_max_read_ledger_entries
        self.ledger_max_read_bytes = ledger_max_read_bytes
        self.ledger_max_write_ledger_entries = ledger_max_write_ledger_entries
        self.ledger_max_write_bytes = ledger_max_write_bytes
        self.tx_max_read_ledger_entries = tx_max_read_ledger_entries
        self.tx_max_read_bytes = tx_max_read_bytes
        self.tx_max_write_ledger_entries = tx_max_write_ledger_entries
        self.tx_max_write_bytes = tx_max_write_bytes
        self.fee_read_ledger_entry = fee_read_ledger_entry
        self.fee_write_ledger_entry = fee_write_ledger_entry
        self.fee_read1_kb = fee_read1_kb
        self.bucket_list_target_size_bytes = bucket_list_target_size_bytes
        self.write_fee1_kb_bucket_list_low = write_fee1_kb_bucket_list_low
        self.write_fee1_kb_bucket_list_high = write_fee1_kb_bucket_list_high
        self.bucket_list_write_fee_growth_factor = bucket_list_write_fee_growth_factor

    def pack(self, packer: Packer) -> None:
        self.ledger_max_read_ledger_entries.pack(packer)
        self.ledger_max_read_bytes.pack(packer)
        self.ledger_max_write_ledger_entries.pack(packer)
        self.ledger_max_write_bytes.pack(packer)
        self.tx_max_read_ledger_entries.pack(packer)
        self.tx_max_read_bytes.pack(packer)
        self.tx_max_write_ledger_entries.pack(packer)
        self.tx_max_write_bytes.pack(packer)
        self.fee_read_ledger_entry.pack(packer)
        self.fee_write_ledger_entry.pack(packer)
        self.fee_read1_kb.pack(packer)
        self.bucket_list_target_size_bytes.pack(packer)
        self.write_fee1_kb_bucket_list_low.pack(packer)
        self.write_fee1_kb_bucket_list_high.pack(packer)
        self.bucket_list_write_fee_growth_factor.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ConfigSettingContractLedgerCostV0:
        ledger_max_read_ledger_entries = Uint32.unpack(unpacker)
        ledger_max_read_bytes = Uint32.unpack(unpacker)
        ledger_max_write_ledger_entries = Uint32.unpack(unpacker)
        ledger_max_write_bytes = Uint32.unpack(unpacker)
        tx_max_read_ledger_entries = Uint32.unpack(unpacker)
        tx_max_read_bytes = Uint32.unpack(unpacker)
        tx_max_write_ledger_entries = Uint32.unpack(unpacker)
        tx_max_write_bytes = Uint32.unpack(unpacker)
        fee_read_ledger_entry = Int64.unpack(unpacker)
        fee_write_ledger_entry = Int64.unpack(unpacker)
        fee_read1_kb = Int64.unpack(unpacker)
        bucket_list_target_size_bytes = Int64.unpack(unpacker)
        write_fee1_kb_bucket_list_low = Int64.unpack(unpacker)
        write_fee1_kb_bucket_list_high = Int64.unpack(unpacker)
        bucket_list_write_fee_growth_factor = Uint32.unpack(unpacker)
        return cls(
            ledger_max_read_ledger_entries=ledger_max_read_ledger_entries,
            ledger_max_read_bytes=ledger_max_read_bytes,
            ledger_max_write_ledger_entries=ledger_max_write_ledger_entries,
            ledger_max_write_bytes=ledger_max_write_bytes,
            tx_max_read_ledger_entries=tx_max_read_ledger_entries,
            tx_max_read_bytes=tx_max_read_bytes,
            tx_max_write_ledger_entries=tx_max_write_ledger_entries,
            tx_max_write_bytes=tx_max_write_bytes,
            fee_read_ledger_entry=fee_read_ledger_entry,
            fee_write_ledger_entry=fee_write_ledger_entry,
            fee_read1_kb=fee_read1_kb,
            bucket_list_target_size_bytes=bucket_list_target_size_bytes,
            write_fee1_kb_bucket_list_low=write_fee1_kb_bucket_list_low,
            write_fee1_kb_bucket_list_high=write_fee1_kb_bucket_list_high,
            bucket_list_write_fee_growth_factor=bucket_list_write_fee_growth_factor,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ConfigSettingContractLedgerCostV0:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ConfigSettingContractLedgerCostV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.ledger_max_read_ledger_entries,
                self.ledger_max_read_bytes,
                self.ledger_max_write_ledger_entries,
                self.ledger_max_write_bytes,
                self.tx_max_read_ledger_entries,
                self.tx_max_read_bytes,
                self.tx_max_write_ledger_entries,
                self.tx_max_write_bytes,
                self.fee_read_ledger_entry,
                self.fee_write_ledger_entry,
                self.fee_read1_kb,
                self.bucket_list_target_size_bytes,
                self.write_fee1_kb_bucket_list_low,
                self.write_fee1_kb_bucket_list_high,
                self.bucket_list_write_fee_growth_factor,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ledger_max_read_ledger_entries == other.ledger_max_read_ledger_entries
            and self.ledger_max_read_bytes == other.ledger_max_read_bytes
            and self.ledger_max_write_ledger_entries
            == other.ledger_max_write_ledger_entries
            and self.ledger_max_write_bytes == other.ledger_max_write_bytes
            and self.tx_max_read_ledger_entries == other.tx_max_read_ledger_entries
            and self.tx_max_read_bytes == other.tx_max_read_bytes
            and self.tx_max_write_ledger_entries == other.tx_max_write_ledger_entries
            and self.tx_max_write_bytes == other.tx_max_write_bytes
            and self.fee_read_ledger_entry == other.fee_read_ledger_entry
            and self.fee_write_ledger_entry == other.fee_write_ledger_entry
            and self.fee_read1_kb == other.fee_read1_kb
            and self.bucket_list_target_size_bytes
            == other.bucket_list_target_size_bytes
            and self.write_fee1_kb_bucket_list_low
            == other.write_fee1_kb_bucket_list_low
            and self.write_fee1_kb_bucket_list_high
            == other.write_fee1_kb_bucket_list_high
            and self.bucket_list_write_fee_growth_factor
            == other.bucket_list_write_fee_growth_factor
        )

    def __repr__(self):
        out = [
            f"ledger_max_read_ledger_entries={self.ledger_max_read_ledger_entries}",
            f"ledger_max_read_bytes={self.ledger_max_read_bytes}",
            f"ledger_max_write_ledger_entries={self.ledger_max_write_ledger_entries}",
            f"ledger_max_write_bytes={self.ledger_max_write_bytes}",
            f"tx_max_read_ledger_entries={self.tx_max_read_ledger_entries}",
            f"tx_max_read_bytes={self.tx_max_read_bytes}",
            f"tx_max_write_ledger_entries={self.tx_max_write_ledger_entries}",
            f"tx_max_write_bytes={self.tx_max_write_bytes}",
            f"fee_read_ledger_entry={self.fee_read_ledger_entry}",
            f"fee_write_ledger_entry={self.fee_write_ledger_entry}",
            f"fee_read1_kb={self.fee_read1_kb}",
            f"bucket_list_target_size_bytes={self.bucket_list_target_size_bytes}",
            f"write_fee1_kb_bucket_list_low={self.write_fee1_kb_bucket_list_low}",
            f"write_fee1_kb_bucket_list_high={self.write_fee1_kb_bucket_list_high}",
            f"bucket_list_write_fee_growth_factor={self.bucket_list_write_fee_growth_factor}",
        ]
        return f"<ConfigSettingContractLedgerCostV0 [{', '.join(out)}]>"
