# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .ledger_header_history_entry import LedgerHeaderHistoryEntry
from .scp_history_entry import SCPHistoryEntry
from .transaction_result_meta import TransactionResultMeta
from .transaction_set import TransactionSet
from .upgrade_entry_meta import UpgradeEntryMeta

__all__ = ["LedgerCloseMetaV0"]


class LedgerCloseMetaV0:
    """
    XDR Source Code::

        struct LedgerCloseMetaV0
        {
            LedgerHeaderHistoryEntry ledgerHeader;
            // NB: txSet is sorted in "Hash order"
            TransactionSet txSet;

            // NB: transactions are sorted in apply order here
            // fees for all transactions are processed first
            // followed by applying transactions
            TransactionResultMeta txProcessing<>;

            // upgrades are applied last
            UpgradeEntryMeta upgradesProcessing<>;

            // other misc information attached to the ledger close
            SCPHistoryEntry scpInfo<>;
        };
    """

    def __init__(
        self,
        ledger_header: LedgerHeaderHistoryEntry,
        tx_set: TransactionSet,
        tx_processing: List[TransactionResultMeta],
        upgrades_processing: List[UpgradeEntryMeta],
        scp_info: List[SCPHistoryEntry],
    ) -> None:
        _expect_max_length = 4294967295
        if tx_processing and len(tx_processing) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `tx_processing` should be {_expect_max_length}, but got {len(tx_processing)}."
            )
        _expect_max_length = 4294967295
        if upgrades_processing and len(upgrades_processing) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `upgrades_processing` should be {_expect_max_length}, but got {len(upgrades_processing)}."
            )
        _expect_max_length = 4294967295
        if scp_info and len(scp_info) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `scp_info` should be {_expect_max_length}, but got {len(scp_info)}."
            )
        self.ledger_header = ledger_header
        self.tx_set = tx_set
        self.tx_processing = tx_processing
        self.upgrades_processing = upgrades_processing
        self.scp_info = scp_info

    def pack(self, packer: Packer) -> None:
        self.ledger_header.pack(packer)
        self.tx_set.pack(packer)
        packer.pack_uint(len(self.tx_processing))
        for tx_processing_item in self.tx_processing:
            tx_processing_item.pack(packer)
        packer.pack_uint(len(self.upgrades_processing))
        for upgrades_processing_item in self.upgrades_processing:
            upgrades_processing_item.pack(packer)
        packer.pack_uint(len(self.scp_info))
        for scp_info_item in self.scp_info:
            scp_info_item.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> LedgerCloseMetaV0:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        ledger_header = LedgerHeaderHistoryEntry.unpack(unpacker, depth_limit - 1)
        tx_set = TransactionSet.unpack(unpacker, depth_limit - 1)
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"tx_processing length {length} exceeds remaining input length {_remaining}"
            )
        tx_processing = []
        for _ in range(length):
            tx_processing.append(
                TransactionResultMeta.unpack(unpacker, depth_limit - 1)
            )
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"upgrades_processing length {length} exceeds remaining input length {_remaining}"
            )
        upgrades_processing = []
        for _ in range(length):
            upgrades_processing.append(
                UpgradeEntryMeta.unpack(unpacker, depth_limit - 1)
            )
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"scp_info length {length} exceeds remaining input length {_remaining}"
            )
        scp_info = []
        for _ in range(length):
            scp_info.append(SCPHistoryEntry.unpack(unpacker, depth_limit - 1))
        return cls(
            ledger_header=ledger_header,
            tx_set=tx_set,
            tx_processing=tx_processing,
            upgrades_processing=upgrades_processing,
            scp_info=scp_info,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerCloseMetaV0:
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
    def from_xdr(cls, xdr: str) -> LedgerCloseMetaV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LedgerCloseMetaV0:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "ledger_header": self.ledger_header.to_json_dict(),
            "tx_set": self.tx_set.to_json_dict(),
            "tx_processing": [item.to_json_dict() for item in self.tx_processing],
            "upgrades_processing": [
                item.to_json_dict() for item in self.upgrades_processing
            ],
            "scp_info": [item.to_json_dict() for item in self.scp_info],
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> LedgerCloseMetaV0:
        ledger_header = LedgerHeaderHistoryEntry.from_json_dict(
            json_dict["ledger_header"]
        )
        tx_set = TransactionSet.from_json_dict(json_dict["tx_set"])
        tx_processing = [
            TransactionResultMeta.from_json_dict(item)
            for item in json_dict["tx_processing"]
        ]
        upgrades_processing = [
            UpgradeEntryMeta.from_json_dict(item)
            for item in json_dict["upgrades_processing"]
        ]
        scp_info = [
            SCPHistoryEntry.from_json_dict(item) for item in json_dict["scp_info"]
        ]
        return cls(
            ledger_header=ledger_header,
            tx_set=tx_set,
            tx_processing=tx_processing,
            upgrades_processing=upgrades_processing,
            scp_info=scp_info,
        )

    def __hash__(self):
        return hash(
            (
                self.ledger_header,
                self.tx_set,
                self.tx_processing,
                self.upgrades_processing,
                self.scp_info,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ledger_header == other.ledger_header
            and self.tx_set == other.tx_set
            and self.tx_processing == other.tx_processing
            and self.upgrades_processing == other.upgrades_processing
            and self.scp_info == other.scp_info
        )

    def __repr__(self):
        out = [
            f"ledger_header={self.ledger_header}",
            f"tx_set={self.tx_set}",
            f"tx_processing={self.tx_processing}",
            f"upgrades_processing={self.upgrades_processing}",
            f"scp_info={self.scp_info}",
        ]
        return f"<LedgerCloseMetaV0 [{', '.join(out)}]>"
