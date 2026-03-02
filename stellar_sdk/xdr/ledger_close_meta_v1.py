# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .generalized_transaction_set import GeneralizedTransactionSet
from .ledger_close_meta_ext import LedgerCloseMetaExt
from .ledger_entry import LedgerEntry
from .ledger_header_history_entry import LedgerHeaderHistoryEntry
from .ledger_key import LedgerKey
from .scp_history_entry import SCPHistoryEntry
from .transaction_result_meta import TransactionResultMeta
from .uint64 import Uint64
from .upgrade_entry_meta import UpgradeEntryMeta

__all__ = ["LedgerCloseMetaV1"]


class LedgerCloseMetaV1:
    """
    XDR Source Code::

        struct LedgerCloseMetaV1
        {
            LedgerCloseMetaExt ext;

            LedgerHeaderHistoryEntry ledgerHeader;

            GeneralizedTransactionSet txSet;

            // NB: transactions are sorted in apply order here
            // fees for all transactions are processed first
            // followed by applying transactions
            TransactionResultMeta txProcessing<>;

            // upgrades are applied last
            UpgradeEntryMeta upgradesProcessing<>;

            // other misc information attached to the ledger close
            SCPHistoryEntry scpInfo<>;

            // Size in bytes of live Soroban state, to support downstream
            // systems calculating storage fees correctly.
            uint64 totalByteSizeOfLiveSorobanState;

            // TTL and data/code keys that have been evicted at this ledger.
            LedgerKey evictedKeys<>;

            // Maintained for backwards compatibility, should never be populated.
            LedgerEntry unused<>;
        };
    """

    def __init__(
        self,
        ext: LedgerCloseMetaExt,
        ledger_header: LedgerHeaderHistoryEntry,
        tx_set: GeneralizedTransactionSet,
        tx_processing: List[TransactionResultMeta],
        upgrades_processing: List[UpgradeEntryMeta],
        scp_info: List[SCPHistoryEntry],
        total_byte_size_of_live_soroban_state: Uint64,
        evicted_keys: List[LedgerKey],
        unused: List[LedgerEntry],
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
        _expect_max_length = 4294967295
        if evicted_keys and len(evicted_keys) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `evicted_keys` should be {_expect_max_length}, but got {len(evicted_keys)}."
            )
        _expect_max_length = 4294967295
        if unused and len(unused) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `unused` should be {_expect_max_length}, but got {len(unused)}."
            )
        self.ext = ext
        self.ledger_header = ledger_header
        self.tx_set = tx_set
        self.tx_processing = tx_processing
        self.upgrades_processing = upgrades_processing
        self.scp_info = scp_info
        self.total_byte_size_of_live_soroban_state = (
            total_byte_size_of_live_soroban_state
        )
        self.evicted_keys = evicted_keys
        self.unused = unused

    def pack(self, packer: Packer) -> None:
        self.ext.pack(packer)
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
        self.total_byte_size_of_live_soroban_state.pack(packer)
        packer.pack_uint(len(self.evicted_keys))
        for evicted_keys_item in self.evicted_keys:
            evicted_keys_item.pack(packer)
        packer.pack_uint(len(self.unused))
        for unused_item in self.unused:
            unused_item.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> LedgerCloseMetaV1:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        ext = LedgerCloseMetaExt.unpack(unpacker, depth_limit - 1)
        ledger_header = LedgerHeaderHistoryEntry.unpack(unpacker, depth_limit - 1)
        tx_set = GeneralizedTransactionSet.unpack(unpacker, depth_limit - 1)
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
        total_byte_size_of_live_soroban_state = Uint64.unpack(unpacker, depth_limit - 1)
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"evicted_keys length {length} exceeds remaining input length {_remaining}"
            )
        evicted_keys = []
        for _ in range(length):
            evicted_keys.append(LedgerKey.unpack(unpacker, depth_limit - 1))
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"unused length {length} exceeds remaining input length {_remaining}"
            )
        unused = []
        for _ in range(length):
            unused.append(LedgerEntry.unpack(unpacker, depth_limit - 1))
        return cls(
            ext=ext,
            ledger_header=ledger_header,
            tx_set=tx_set,
            tx_processing=tx_processing,
            upgrades_processing=upgrades_processing,
            scp_info=scp_info,
            total_byte_size_of_live_soroban_state=total_byte_size_of_live_soroban_state,
            evicted_keys=evicted_keys,
            unused=unused,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerCloseMetaV1:
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
    def from_xdr(cls, xdr: str) -> LedgerCloseMetaV1:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LedgerCloseMetaV1:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "ext": self.ext.to_json_dict(),
            "ledger_header": self.ledger_header.to_json_dict(),
            "tx_set": self.tx_set.to_json_dict(),
            "tx_processing": [item.to_json_dict() for item in self.tx_processing],
            "upgrades_processing": [
                item.to_json_dict() for item in self.upgrades_processing
            ],
            "scp_info": [item.to_json_dict() for item in self.scp_info],
            "total_byte_size_of_live_soroban_state": self.total_byte_size_of_live_soroban_state.to_json_dict(),
            "evicted_keys": [item.to_json_dict() for item in self.evicted_keys],
            "unused": [item.to_json_dict() for item in self.unused],
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> LedgerCloseMetaV1:
        ext = LedgerCloseMetaExt.from_json_dict(json_dict["ext"])
        ledger_header = LedgerHeaderHistoryEntry.from_json_dict(
            json_dict["ledger_header"]
        )
        tx_set = GeneralizedTransactionSet.from_json_dict(json_dict["tx_set"])
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
        total_byte_size_of_live_soroban_state = Uint64.from_json_dict(
            json_dict["total_byte_size_of_live_soroban_state"]
        )
        evicted_keys = [
            LedgerKey.from_json_dict(item) for item in json_dict["evicted_keys"]
        ]
        unused = [LedgerEntry.from_json_dict(item) for item in json_dict["unused"]]
        return cls(
            ext=ext,
            ledger_header=ledger_header,
            tx_set=tx_set,
            tx_processing=tx_processing,
            upgrades_processing=upgrades_processing,
            scp_info=scp_info,
            total_byte_size_of_live_soroban_state=total_byte_size_of_live_soroban_state,
            evicted_keys=evicted_keys,
            unused=unused,
        )

    def __hash__(self):
        return hash(
            (
                self.ext,
                self.ledger_header,
                self.tx_set,
                self.tx_processing,
                self.upgrades_processing,
                self.scp_info,
                self.total_byte_size_of_live_soroban_state,
                self.evicted_keys,
                self.unused,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ext == other.ext
            and self.ledger_header == other.ledger_header
            and self.tx_set == other.tx_set
            and self.tx_processing == other.tx_processing
            and self.upgrades_processing == other.upgrades_processing
            and self.scp_info == other.scp_info
            and self.total_byte_size_of_live_soroban_state
            == other.total_byte_size_of_live_soroban_state
            and self.evicted_keys == other.evicted_keys
            and self.unused == other.unused
        )

    def __repr__(self):
        out = [
            f"ext={self.ext}",
            f"ledger_header={self.ledger_header}",
            f"tx_set={self.tx_set}",
            f"tx_processing={self.tx_processing}",
            f"upgrades_processing={self.upgrades_processing}",
            f"scp_info={self.scp_info}",
            f"total_byte_size_of_live_soroban_state={self.total_byte_size_of_live_soroban_state}",
            f"evicted_keys={self.evicted_keys}",
            f"unused={self.unused}",
        ]
        return f"<LedgerCloseMetaV1 [{', '.join(out)}]>"
