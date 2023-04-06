# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib import Packer, Unpacker

from .hash import Hash
from .ledger_entry_changes import LedgerEntryChanges
from .operation_diagnostic_events import OperationDiagnosticEvents
from .operation_events import OperationEvents
from .operation_meta import OperationMeta
from .transaction_result import TransactionResult

__all__ = ["TransactionMetaV3"]


class TransactionMetaV3:
    """
    XDR Source Code::

        struct TransactionMetaV3
        {
            LedgerEntryChanges txChangesBefore; // tx level changes before operations
                                                // are applied if any
            OperationMeta operations<>;         // meta for each operation
            LedgerEntryChanges txChangesAfter;  // tx level changes after operations are
                                                // applied if any
            OperationEvents events<>;           // custom events populated by the
                                                // contracts themselves. One list per operation.
            TransactionResult txResult;

            Hash hashes[3];                     // stores sha256(txChangesBefore, operations, txChangesAfter),
                                                // sha256(events), and sha256(txResult)

            // Diagnostics events that are not hashed. One list per operation.
            // This will contain all contract and diagnostic events. Even ones
            // that were emitted in a failed contract call.
            OperationDiagnosticEvents diagnosticEvents<>;
        };
    """

    def __init__(
        self,
        tx_changes_before: LedgerEntryChanges,
        operations: List[OperationMeta],
        tx_changes_after: LedgerEntryChanges,
        events: List[OperationEvents],
        tx_result: TransactionResult,
        hashes: List[Hash],
        diagnostic_events: List[OperationDiagnosticEvents],
    ) -> None:
        _expect_max_length = 4294967295
        if operations and len(operations) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `operations` should be {_expect_max_length}, but got {len(operations)}."
            )
        _expect_max_length = 4294967295
        if events and len(events) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `events` should be {_expect_max_length}, but got {len(events)}."
            )
        _expect_length = 3
        if hashes and len(hashes) != _expect_length:
            raise ValueError(
                f"The length of `hashes` should be {_expect_length}, but got {len(hashes)}."
            )
        _expect_max_length = 4294967295
        if diagnostic_events and len(diagnostic_events) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `diagnostic_events` should be {_expect_max_length}, but got {len(diagnostic_events)}."
            )
        self.tx_changes_before = tx_changes_before
        self.operations = operations
        self.tx_changes_after = tx_changes_after
        self.events = events
        self.tx_result = tx_result
        self.hashes = hashes
        self.diagnostic_events = diagnostic_events

    def pack(self, packer: Packer) -> None:
        self.tx_changes_before.pack(packer)
        packer.pack_uint(len(self.operations))
        for operations_item in self.operations:
            operations_item.pack(packer)
        self.tx_changes_after.pack(packer)
        packer.pack_uint(len(self.events))
        for events_item in self.events:
            events_item.pack(packer)
        self.tx_result.pack(packer)
        for hashes_item in self.hashes:
            hashes_item.pack(packer)
        packer.pack_uint(len(self.diagnostic_events))
        for diagnostic_events_item in self.diagnostic_events:
            diagnostic_events_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionMetaV3":
        tx_changes_before = LedgerEntryChanges.unpack(unpacker)
        length = unpacker.unpack_uint()
        operations = []
        for _ in range(length):
            operations.append(OperationMeta.unpack(unpacker))
        tx_changes_after = LedgerEntryChanges.unpack(unpacker)
        length = unpacker.unpack_uint()
        events = []
        for _ in range(length):
            events.append(OperationEvents.unpack(unpacker))
        tx_result = TransactionResult.unpack(unpacker)
        length = 3
        hashes = []
        for _ in range(length):
            hashes.append(Hash.unpack(unpacker))
        length = unpacker.unpack_uint()
        diagnostic_events = []
        for _ in range(length):
            diagnostic_events.append(OperationDiagnosticEvents.unpack(unpacker))
        return cls(
            tx_changes_before=tx_changes_before,
            operations=operations,
            tx_changes_after=tx_changes_after,
            events=events,
            tx_result=tx_result,
            hashes=hashes,
            diagnostic_events=diagnostic_events,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "TransactionMetaV3":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionMetaV3":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.tx_changes_before == other.tx_changes_before
            and self.operations == other.operations
            and self.tx_changes_after == other.tx_changes_after
            and self.events == other.events
            and self.tx_result == other.tx_result
            and self.hashes == other.hashes
            and self.diagnostic_events == other.diagnostic_events
        )

    def __str__(self):
        out = [
            f"tx_changes_before={self.tx_changes_before}",
            f"operations={self.operations}",
            f"tx_changes_after={self.tx_changes_after}",
            f"events={self.events}",
            f"tx_result={self.tx_result}",
            f"hashes={self.hashes}",
            f"diagnostic_events={self.diagnostic_events}",
        ]
        return f"<TransactionMetaV3 [{', '.join(out)}]>"
