# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib import Packer, Unpacker

from .ledger_header_history_entry import LedgerHeaderHistoryEntry
from .scp_history_entry import SCPHistoryEntry
from .transaction_result_meta import TransactionResultMeta
from .transaction_set import TransactionSet
from .upgrade_entry_meta import UpgradeEntryMeta
from ..exceptions import ValueError

__all__ = ["LedgerCloseMetaV0"]


class LedgerCloseMetaV0:
    """
    XDR Source Code
    ----------------------------------------------------------------
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
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        ledger_header: LedgerHeaderHistoryEntry,
        tx_set: TransactionSet,
        tx_processing: List[TransactionResultMeta],
        upgrades_processing: List[UpgradeEntryMeta],
        scp_info: List[SCPHistoryEntry],
    ) -> None:
        if tx_processing and len(tx_processing) > 4294967295:
            raise ValueError(
                f"The maximum length of `tx_processing` should be 4294967295, but got {len(tx_processing)}."
            )
        if upgrades_processing and len(upgrades_processing) > 4294967295:
            raise ValueError(
                f"The maximum length of `upgrades_processing` should be 4294967295, but got {len(upgrades_processing)}."
            )
        if scp_info and len(scp_info) > 4294967295:
            raise ValueError(
                f"The maximum length of `scp_info` should be 4294967295, but got {len(scp_info)}."
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
        for tx_processing in self.tx_processing:
            tx_processing.pack(packer)
        packer.pack_uint(len(self.upgrades_processing))
        for upgrades_processing in self.upgrades_processing:
            upgrades_processing.pack(packer)
        packer.pack_uint(len(self.scp_info))
        for scp_info in self.scp_info:
            scp_info.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerCloseMetaV0":
        ledger_header = LedgerHeaderHistoryEntry.unpack(unpacker)
        tx_set = TransactionSet.unpack(unpacker)
        length = unpacker.unpack_uint()
        tx_processing = []
        for _ in range(length):
            tx_processing.append(TransactionResultMeta.unpack(unpacker))
        length = unpacker.unpack_uint()
        upgrades_processing = []
        for _ in range(length):
            upgrades_processing.append(UpgradeEntryMeta.unpack(unpacker))
        length = unpacker.unpack_uint()
        scp_info = []
        for _ in range(length):
            scp_info.append(SCPHistoryEntry.unpack(unpacker))
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
    def from_xdr_bytes(cls, xdr: bytes) -> "LedgerCloseMetaV0":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerCloseMetaV0":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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

    def __str__(self):
        out = [
            f"ledger_header={self.ledger_header}",
            f"tx_set={self.tx_set}",
            f"tx_processing={self.tx_processing}",
            f"upgrades_processing={self.upgrades_processing}",
            f"scp_info={self.scp_info}",
        ]
        return f"<LedgerCloseMetaV0 {[', '.join(out)]}>"
