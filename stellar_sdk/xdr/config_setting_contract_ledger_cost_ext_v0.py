# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .int64 import Int64
from .uint32 import Uint32

__all__ = ["ConfigSettingContractLedgerCostExtV0"]


class ConfigSettingContractLedgerCostExtV0:
    """
    XDR Source Code::

        struct ConfigSettingContractLedgerCostExtV0
        {
            // Maximum number of RO+RW entries in the transaction footprint.
            uint32 txMaxFootprintEntries;
            // Fee per 1 KB of data written to the ledger.
            // Unlike the rent fee, this is a flat fee that is charged for any ledger
            // write, independent of the type of the entry being written.
            int64 feeWrite1KB;
        };
    """

    def __init__(
        self,
        tx_max_footprint_entries: Uint32,
        fee_write1_kb: Int64,
    ) -> None:
        self.tx_max_footprint_entries = tx_max_footprint_entries
        self.fee_write1_kb = fee_write1_kb

    def pack(self, packer: Packer) -> None:
        self.tx_max_footprint_entries.pack(packer)
        self.fee_write1_kb.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ConfigSettingContractLedgerCostExtV0:
        tx_max_footprint_entries = Uint32.unpack(unpacker)
        fee_write1_kb = Int64.unpack(unpacker)
        return cls(
            tx_max_footprint_entries=tx_max_footprint_entries,
            fee_write1_kb=fee_write1_kb,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ConfigSettingContractLedgerCostExtV0:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ConfigSettingContractLedgerCostExtV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.tx_max_footprint_entries,
                self.fee_write1_kb,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.tx_max_footprint_entries == other.tx_max_footprint_entries
            and self.fee_write1_kb == other.fee_write1_kb
        )

    def __repr__(self):
        out = [
            f"tx_max_footprint_entries={self.tx_max_footprint_entries}",
            f"fee_write1_kb={self.fee_write1_kb}",
        ]
        return f"<ConfigSettingContractLedgerCostExtV0 [{', '.join(out)}]>"
