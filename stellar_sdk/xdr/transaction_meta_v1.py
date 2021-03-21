# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib import Packer, Unpacker

from .ledger_entry_changes import LedgerEntryChanges
from .operation_meta import OperationMeta
from ..exceptions import ValueError

__all__ = ["TransactionMetaV1"]


class TransactionMetaV1:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct TransactionMetaV1
    {
        LedgerEntryChanges txChanges; // tx level changes if any
        OperationMeta operations<>;   // meta for each operation
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        tx_changes: LedgerEntryChanges,
        operations: List[OperationMeta],
    ) -> None:
        if operations and len(operations) > 4294967295:
            raise ValueError(
                f"The maximum length of `operations` should be 4294967295, but got {len(operations)}."
            )
        self.tx_changes = tx_changes
        self.operations = operations

    def pack(self, packer: Packer) -> None:
        self.tx_changes.pack(packer)
        packer.pack_uint(len(self.operations))
        for operation in self.operations:
            operation.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionMetaV1":
        tx_changes = LedgerEntryChanges.unpack(unpacker)
        length = unpacker.unpack_uint()
        operations = []
        for _ in range(length):
            operations.append(OperationMeta.unpack(unpacker))
        return cls(
            tx_changes=tx_changes,
            operations=operations,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "TransactionMetaV1":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionMetaV1":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.tx_changes == other.tx_changes and self.operations == other.operations
        )

    def __str__(self):
        out = [
            f"tx_changes={self.tx_changes}",
            f"operations={self.operations}",
        ]
        return f"<TransactionMetaV1 {[', '.join(out)]}>"
