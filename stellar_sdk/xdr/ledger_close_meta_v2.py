# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

from .generalized_transaction_set import GeneralizedTransactionSet
from .ledger_close_meta_ext import LedgerCloseMetaExt
from .ledger_header_history_entry import LedgerHeaderHistoryEntry
from .ledger_key import LedgerKey
from .scp_history_entry import SCPHistoryEntry
from .transaction_result_meta_v1 import TransactionResultMetaV1
from .uint64 import Uint64
from .upgrade_entry_meta import UpgradeEntryMeta

__all__ = ["LedgerCloseMetaV2"]


class LedgerCloseMetaV2:
    """
    XDR Source Code::

        struct LedgerCloseMetaV2
        {
            LedgerCloseMetaExt ext;

            LedgerHeaderHistoryEntry ledgerHeader;

            GeneralizedTransactionSet txSet;

            // NB: transactions are sorted in apply order here
            // fees for all transactions are processed first
            // followed by applying transactions
            TransactionResultMetaV1 txProcessing<>;

            // upgrades are applied last
            UpgradeEntryMeta upgradesProcessing<>;

            // other misc information attached to the ledger close
            SCPHistoryEntry scpInfo<>;

            // Size in bytes of live Soroban state, to support downstream
            // systems calculating storage fees correctly.
            uint64 totalByteSizeOfLiveSorobanState;

            // TTL and data/code keys that have been evicted at this ledger.
            LedgerKey evictedKeys<>;
        };
    """

    def __init__(
        self,
        ext: LedgerCloseMetaExt,
        ledger_header: LedgerHeaderHistoryEntry,
        tx_set: GeneralizedTransactionSet,
        tx_processing: List[TransactionResultMetaV1],
        upgrades_processing: List[UpgradeEntryMeta],
        scp_info: List[SCPHistoryEntry],
        total_byte_size_of_live_soroban_state: Uint64,
        evicted_keys: List[LedgerKey],
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

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> LedgerCloseMetaV2:
        ext = LedgerCloseMetaExt.unpack(unpacker)
        ledger_header = LedgerHeaderHistoryEntry.unpack(unpacker)
        tx_set = GeneralizedTransactionSet.unpack(unpacker)
        length = unpacker.unpack_uint()
        tx_processing = []
        for _ in range(length):
            tx_processing.append(TransactionResultMetaV1.unpack(unpacker))
        length = unpacker.unpack_uint()
        upgrades_processing = []
        for _ in range(length):
            upgrades_processing.append(UpgradeEntryMeta.unpack(unpacker))
        length = unpacker.unpack_uint()
        scp_info = []
        for _ in range(length):
            scp_info.append(SCPHistoryEntry.unpack(unpacker))
        total_byte_size_of_live_soroban_state = Uint64.unpack(unpacker)
        length = unpacker.unpack_uint()
        evicted_keys = []
        for _ in range(length):
            evicted_keys.append(LedgerKey.unpack(unpacker))
        return cls(
            ext=ext,
            ledger_header=ledger_header,
            tx_set=tx_set,
            tx_processing=tx_processing,
            upgrades_processing=upgrades_processing,
            scp_info=scp_info,
            total_byte_size_of_live_soroban_state=total_byte_size_of_live_soroban_state,
            evicted_keys=evicted_keys,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerCloseMetaV2:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LedgerCloseMetaV2:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
        ]
        return f"<LedgerCloseMetaV2 [{', '.join(out)}]>"
