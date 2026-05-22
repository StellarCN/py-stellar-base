# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ConfigSettingContractLedgerCostExtV0:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        tx_max_footprint_entries = Uint32.unpack(unpacker, depth_limit - 1)
        fee_write1_kb = Int64.unpack(unpacker, depth_limit - 1)
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ConfigSettingContractLedgerCostExtV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ConfigSettingContractLedgerCostExtV0:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "tx_max_footprint_entries": self.tx_max_footprint_entries.to_json_dict(),
            "fee_write1_kb": self.fee_write1_kb.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> ConfigSettingContractLedgerCostExtV0:
        tx_max_footprint_entries = Uint32.from_json_dict(
            json_dict["tx_max_footprint_entries"]
        )
        fee_write1_kb = Int64.from_json_dict(json_dict["fee_write1_kb"])
        return cls(
            tx_max_footprint_entries=tx_max_footprint_entries,
            fee_write1_kb=fee_write1_kb,
        )

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
