# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib import Packer, Unpacker

from .ledger_entry_changes import LedgerEntryChanges
from .operation_meta import OperationMeta
from ..exceptions import ValueError

__all__ = ["TransactionMetaV2"]


class TransactionMetaV2:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct TransactionMetaV2
    {
        LedgerEntryChanges txChangesBefore; // tx level changes before operations
                                            // are applied if any
        OperationMeta operations<>;         // meta for each operation
        LedgerEntryChanges txChangesAfter;  // tx level changes after operations are
                                            // applied if any
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        tx_changes_before: LedgerEntryChanges,
        operations: List[OperationMeta],
        tx_changes_after: LedgerEntryChanges,
    ) -> None:
        if operations and len(operations) > 4294967295:
            raise ValueError(
                f"The maximum length of `operations` should be 4294967295, but got {len(operations)}."
            )
        self.tx_changes_before = tx_changes_before
        self.operations = operations
        self.tx_changes_after = tx_changes_after

    def pack(self, packer: Packer) -> None:
        self.tx_changes_before.pack(packer)
        packer.pack_uint(len(self.operations))
        for operation in self.operations:
            operation.pack(packer)
        self.tx_changes_after.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionMetaV2":
        tx_changes_before = LedgerEntryChanges.unpack(unpacker)
        length = unpacker.unpack_uint()
        operations = []
        for _ in range(length):
            operations.append(OperationMeta.unpack(unpacker))
        tx_changes_after = LedgerEntryChanges.unpack(unpacker)
        return cls(
            tx_changes_before=tx_changes_before,
            operations=operations,
            tx_changes_after=tx_changes_after,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "TransactionMetaV2":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionMetaV2":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.tx_changes_before == other.tx_changes_before
            and self.operations == other.operations
            and self.tx_changes_after == other.tx_changes_after
        )

    def __str__(self):
        out = [
            f"tx_changes_before={self.tx_changes_before}",
            f"operations={self.operations}",
            f"tx_changes_after={self.tx_changes_after}",
        ]
        return f"<TransactionMetaV2 {[', '.join(out)]}>"
