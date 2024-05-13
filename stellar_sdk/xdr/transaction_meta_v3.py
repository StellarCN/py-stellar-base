# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List, Optional

from xdrlib3 import Packer, Unpacker

from .extension_point import ExtensionPoint
from .ledger_entry_changes import LedgerEntryChanges
from .operation_meta import OperationMeta
from .soroban_transaction_meta import SorobanTransactionMeta

__all__ = ["TransactionMetaV3"]


class TransactionMetaV3:
    """
    XDR Source Code::

        struct TransactionMetaV3
        {
            ExtensionPoint ext;

            LedgerEntryChanges txChangesBefore;  // tx level changes before operations
                                                 // are applied if any
            OperationMeta operations<>;          // meta for each operation
            LedgerEntryChanges txChangesAfter;   // tx level changes after operations are
                                                 // applied if any
            SorobanTransactionMeta* sorobanMeta; // Soroban-specific meta (only for
                                                 // Soroban transactions).
        };
    """

    def __init__(
        self,
        ext: ExtensionPoint,
        tx_changes_before: LedgerEntryChanges,
        operations: List[OperationMeta],
        tx_changes_after: LedgerEntryChanges,
        soroban_meta: Optional[SorobanTransactionMeta],
    ) -> None:
        _expect_max_length = 4294967295
        if operations and len(operations) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `operations` should be {_expect_max_length}, but got {len(operations)}."
            )
        self.ext = ext
        self.tx_changes_before = tx_changes_before
        self.operations = operations
        self.tx_changes_after = tx_changes_after
        self.soroban_meta = soroban_meta

    def pack(self, packer: Packer) -> None:
        self.ext.pack(packer)
        self.tx_changes_before.pack(packer)
        packer.pack_uint(len(self.operations))
        for operations_item in self.operations:
            operations_item.pack(packer)
        self.tx_changes_after.pack(packer)
        if self.soroban_meta is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.soroban_meta.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> TransactionMetaV3:
        ext = ExtensionPoint.unpack(unpacker)
        tx_changes_before = LedgerEntryChanges.unpack(unpacker)
        length = unpacker.unpack_uint()
        operations = []
        for _ in range(length):
            operations.append(OperationMeta.unpack(unpacker))
        tx_changes_after = LedgerEntryChanges.unpack(unpacker)
        soroban_meta = (
            SorobanTransactionMeta.unpack(unpacker) if unpacker.unpack_uint() else None
        )
        return cls(
            ext=ext,
            tx_changes_before=tx_changes_before,
            operations=operations,
            tx_changes_after=tx_changes_after,
            soroban_meta=soroban_meta,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TransactionMetaV3:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> TransactionMetaV3:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.ext,
                self.tx_changes_before,
                self.operations,
                self.tx_changes_after,
                self.soroban_meta,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ext == other.ext
            and self.tx_changes_before == other.tx_changes_before
            and self.operations == other.operations
            and self.tx_changes_after == other.tx_changes_after
            and self.soroban_meta == other.soroban_meta
        )

    def __repr__(self):
        out = [
            f"ext={self.ext}",
            f"tx_changes_before={self.tx_changes_before}",
            f"operations={self.operations}",
            f"tx_changes_after={self.tx_changes_after}",
            f"soroban_meta={self.soroban_meta}",
        ]
        return f"<TransactionMetaV3 [{', '.join(out)}]>"
