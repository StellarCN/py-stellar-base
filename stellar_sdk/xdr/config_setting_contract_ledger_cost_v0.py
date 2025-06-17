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
            // Maximum number of disk entry read operations per ledger
            uint32 ledgerMaxDiskReadEntries;
            // Maximum number of bytes of disk reads that can be performed per ledger
            uint32 ledgerMaxDiskReadBytes;
            // Maximum number of ledger entry write operations per ledger
            uint32 ledgerMaxWriteLedgerEntries;
            // Maximum number of bytes that can be written per ledger
            uint32 ledgerMaxWriteBytes;

            // Maximum number of disk entry read operations per transaction
            uint32 txMaxDiskReadEntries;
            // Maximum number of bytes of disk reads that can be performed per transaction
            uint32 txMaxDiskReadBytes;
            // Maximum number of ledger entry write operations per transaction
            uint32 txMaxWriteLedgerEntries;
            // Maximum number of bytes that can be written per transaction
            uint32 txMaxWriteBytes;

            int64 feeDiskReadLedgerEntry;  // Fee per disk ledger entry read
            int64 feeWriteLedgerEntry;     // Fee per ledger entry write

            int64 feeDiskRead1KB;          // Fee for reading 1KB disk

            // The following parameters determine the write fee per 1KB.
            // Rent fee grows linearly until soroban state reaches this size
            int64 sorobanStateTargetSizeBytes;
            // Fee per 1KB rent when the soroban state is empty
            int64 rentFee1KBSorobanStateSizeLow;
            // Fee per 1KB rent when the soroban state has reached `sorobanStateTargetSizeBytes`
            int64 rentFee1KBSorobanStateSizeHigh;
            // Rent fee multiplier for any additional data past the first `sorobanStateTargetSizeBytes`
            uint32 sorobanStateRentFeeGrowthFactor;
        };
    """

    def __init__(
        self,
        ledger_max_disk_read_entries: Uint32,
        ledger_max_disk_read_bytes: Uint32,
        ledger_max_write_ledger_entries: Uint32,
        ledger_max_write_bytes: Uint32,
        tx_max_disk_read_entries: Uint32,
        tx_max_disk_read_bytes: Uint32,
        tx_max_write_ledger_entries: Uint32,
        tx_max_write_bytes: Uint32,
        fee_disk_read_ledger_entry: Int64,
        fee_write_ledger_entry: Int64,
        fee_disk_read1_kb: Int64,
        soroban_state_target_size_bytes: Int64,
        rent_fee1_kb_soroban_state_size_low: Int64,
        rent_fee1_kb_soroban_state_size_high: Int64,
        soroban_state_rent_fee_growth_factor: Uint32,
    ) -> None:
        self.ledger_max_disk_read_entries = ledger_max_disk_read_entries
        self.ledger_max_disk_read_bytes = ledger_max_disk_read_bytes
        self.ledger_max_write_ledger_entries = ledger_max_write_ledger_entries
        self.ledger_max_write_bytes = ledger_max_write_bytes
        self.tx_max_disk_read_entries = tx_max_disk_read_entries
        self.tx_max_disk_read_bytes = tx_max_disk_read_bytes
        self.tx_max_write_ledger_entries = tx_max_write_ledger_entries
        self.tx_max_write_bytes = tx_max_write_bytes
        self.fee_disk_read_ledger_entry = fee_disk_read_ledger_entry
        self.fee_write_ledger_entry = fee_write_ledger_entry
        self.fee_disk_read1_kb = fee_disk_read1_kb
        self.soroban_state_target_size_bytes = soroban_state_target_size_bytes
        self.rent_fee1_kb_soroban_state_size_low = rent_fee1_kb_soroban_state_size_low
        self.rent_fee1_kb_soroban_state_size_high = rent_fee1_kb_soroban_state_size_high
        self.soroban_state_rent_fee_growth_factor = soroban_state_rent_fee_growth_factor

    def pack(self, packer: Packer) -> None:
        self.ledger_max_disk_read_entries.pack(packer)
        self.ledger_max_disk_read_bytes.pack(packer)
        self.ledger_max_write_ledger_entries.pack(packer)
        self.ledger_max_write_bytes.pack(packer)
        self.tx_max_disk_read_entries.pack(packer)
        self.tx_max_disk_read_bytes.pack(packer)
        self.tx_max_write_ledger_entries.pack(packer)
        self.tx_max_write_bytes.pack(packer)
        self.fee_disk_read_ledger_entry.pack(packer)
        self.fee_write_ledger_entry.pack(packer)
        self.fee_disk_read1_kb.pack(packer)
        self.soroban_state_target_size_bytes.pack(packer)
        self.rent_fee1_kb_soroban_state_size_low.pack(packer)
        self.rent_fee1_kb_soroban_state_size_high.pack(packer)
        self.soroban_state_rent_fee_growth_factor.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ConfigSettingContractLedgerCostV0:
        ledger_max_disk_read_entries = Uint32.unpack(unpacker)
        ledger_max_disk_read_bytes = Uint32.unpack(unpacker)
        ledger_max_write_ledger_entries = Uint32.unpack(unpacker)
        ledger_max_write_bytes = Uint32.unpack(unpacker)
        tx_max_disk_read_entries = Uint32.unpack(unpacker)
        tx_max_disk_read_bytes = Uint32.unpack(unpacker)
        tx_max_write_ledger_entries = Uint32.unpack(unpacker)
        tx_max_write_bytes = Uint32.unpack(unpacker)
        fee_disk_read_ledger_entry = Int64.unpack(unpacker)
        fee_write_ledger_entry = Int64.unpack(unpacker)
        fee_disk_read1_kb = Int64.unpack(unpacker)
        soroban_state_target_size_bytes = Int64.unpack(unpacker)
        rent_fee1_kb_soroban_state_size_low = Int64.unpack(unpacker)
        rent_fee1_kb_soroban_state_size_high = Int64.unpack(unpacker)
        soroban_state_rent_fee_growth_factor = Uint32.unpack(unpacker)
        return cls(
            ledger_max_disk_read_entries=ledger_max_disk_read_entries,
            ledger_max_disk_read_bytes=ledger_max_disk_read_bytes,
            ledger_max_write_ledger_entries=ledger_max_write_ledger_entries,
            ledger_max_write_bytes=ledger_max_write_bytes,
            tx_max_disk_read_entries=tx_max_disk_read_entries,
            tx_max_disk_read_bytes=tx_max_disk_read_bytes,
            tx_max_write_ledger_entries=tx_max_write_ledger_entries,
            tx_max_write_bytes=tx_max_write_bytes,
            fee_disk_read_ledger_entry=fee_disk_read_ledger_entry,
            fee_write_ledger_entry=fee_write_ledger_entry,
            fee_disk_read1_kb=fee_disk_read1_kb,
            soroban_state_target_size_bytes=soroban_state_target_size_bytes,
            rent_fee1_kb_soroban_state_size_low=rent_fee1_kb_soroban_state_size_low,
            rent_fee1_kb_soroban_state_size_high=rent_fee1_kb_soroban_state_size_high,
            soroban_state_rent_fee_growth_factor=soroban_state_rent_fee_growth_factor,
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
                self.ledger_max_disk_read_entries,
                self.ledger_max_disk_read_bytes,
                self.ledger_max_write_ledger_entries,
                self.ledger_max_write_bytes,
                self.tx_max_disk_read_entries,
                self.tx_max_disk_read_bytes,
                self.tx_max_write_ledger_entries,
                self.tx_max_write_bytes,
                self.fee_disk_read_ledger_entry,
                self.fee_write_ledger_entry,
                self.fee_disk_read1_kb,
                self.soroban_state_target_size_bytes,
                self.rent_fee1_kb_soroban_state_size_low,
                self.rent_fee1_kb_soroban_state_size_high,
                self.soroban_state_rent_fee_growth_factor,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ledger_max_disk_read_entries == other.ledger_max_disk_read_entries
            and self.ledger_max_disk_read_bytes == other.ledger_max_disk_read_bytes
            and self.ledger_max_write_ledger_entries
            == other.ledger_max_write_ledger_entries
            and self.ledger_max_write_bytes == other.ledger_max_write_bytes
            and self.tx_max_disk_read_entries == other.tx_max_disk_read_entries
            and self.tx_max_disk_read_bytes == other.tx_max_disk_read_bytes
            and self.tx_max_write_ledger_entries == other.tx_max_write_ledger_entries
            and self.tx_max_write_bytes == other.tx_max_write_bytes
            and self.fee_disk_read_ledger_entry == other.fee_disk_read_ledger_entry
            and self.fee_write_ledger_entry == other.fee_write_ledger_entry
            and self.fee_disk_read1_kb == other.fee_disk_read1_kb
            and self.soroban_state_target_size_bytes
            == other.soroban_state_target_size_bytes
            and self.rent_fee1_kb_soroban_state_size_low
            == other.rent_fee1_kb_soroban_state_size_low
            and self.rent_fee1_kb_soroban_state_size_high
            == other.rent_fee1_kb_soroban_state_size_high
            and self.soroban_state_rent_fee_growth_factor
            == other.soroban_state_rent_fee_growth_factor
        )

    def __repr__(self):
        out = [
            f"ledger_max_disk_read_entries={self.ledger_max_disk_read_entries}",
            f"ledger_max_disk_read_bytes={self.ledger_max_disk_read_bytes}",
            f"ledger_max_write_ledger_entries={self.ledger_max_write_ledger_entries}",
            f"ledger_max_write_bytes={self.ledger_max_write_bytes}",
            f"tx_max_disk_read_entries={self.tx_max_disk_read_entries}",
            f"tx_max_disk_read_bytes={self.tx_max_disk_read_bytes}",
            f"tx_max_write_ledger_entries={self.tx_max_write_ledger_entries}",
            f"tx_max_write_bytes={self.tx_max_write_bytes}",
            f"fee_disk_read_ledger_entry={self.fee_disk_read_ledger_entry}",
            f"fee_write_ledger_entry={self.fee_write_ledger_entry}",
            f"fee_disk_read1_kb={self.fee_disk_read1_kb}",
            f"soroban_state_target_size_bytes={self.soroban_state_target_size_bytes}",
            f"rent_fee1_kb_soroban_state_size_low={self.rent_fee1_kb_soroban_state_size_low}",
            f"rent_fee1_kb_soroban_state_size_high={self.rent_fee1_kb_soroban_state_size_high}",
            f"soroban_state_rent_fee_growth_factor={self.soroban_state_rent_fee_growth_factor}",
        ]
        return f"<ConfigSettingContractLedgerCostV0 [{', '.join(out)}]>"
