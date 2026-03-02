# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .ledger_entry_changes import LedgerEntryChanges
from .operation_meta import OperationMeta

__all__ = ["TransactionMetaV2"]


class TransactionMetaV2:
    """
    XDR Source Code::

        struct TransactionMetaV2
        {
            LedgerEntryChanges txChangesBefore; // tx level changes before operations
                                                // are applied if any
            OperationMeta operations<>;         // meta for each operation
            LedgerEntryChanges txChangesAfter;  // tx level changes after operations are
                                                // applied if any
        };
    """

    def __init__(
        self,
        tx_changes_before: LedgerEntryChanges,
        operations: List[OperationMeta],
        tx_changes_after: LedgerEntryChanges,
    ) -> None:
        _expect_max_length = 4294967295
        if operations and len(operations) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `operations` should be {_expect_max_length}, but got {len(operations)}."
            )
        self.tx_changes_before = tx_changes_before
        self.operations = operations
        self.tx_changes_after = tx_changes_after

    def pack(self, packer: Packer) -> None:
        self.tx_changes_before.pack(packer)
        packer.pack_uint(len(self.operations))
        for operations_item in self.operations:
            operations_item.pack(packer)
        self.tx_changes_after.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> TransactionMetaV2:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        tx_changes_before = LedgerEntryChanges.unpack(unpacker, depth_limit - 1)
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"operations length {length} exceeds remaining input length {_remaining}"
            )
        operations = []
        for _ in range(length):
            operations.append(OperationMeta.unpack(unpacker, depth_limit - 1))
        tx_changes_after = LedgerEntryChanges.unpack(unpacker, depth_limit - 1)
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
    def from_xdr_bytes(cls, xdr: bytes) -> TransactionMetaV2:
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
    def from_xdr(cls, xdr: str) -> TransactionMetaV2:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TransactionMetaV2:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "tx_changes_before": self.tx_changes_before.to_json_dict(),
            "operations": [item.to_json_dict() for item in self.operations],
            "tx_changes_after": self.tx_changes_after.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> TransactionMetaV2:
        tx_changes_before = LedgerEntryChanges.from_json_dict(
            json_dict["tx_changes_before"]
        )
        operations = [
            OperationMeta.from_json_dict(item) for item in json_dict["operations"]
        ]
        tx_changes_after = LedgerEntryChanges.from_json_dict(
            json_dict["tx_changes_after"]
        )
        return cls(
            tx_changes_before=tx_changes_before,
            operations=operations,
            tx_changes_after=tx_changes_after,
        )

    def __hash__(self):
        return hash(
            (
                self.tx_changes_before,
                self.operations,
                self.tx_changes_after,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.tx_changes_before == other.tx_changes_before
            and self.operations == other.operations
            and self.tx_changes_after == other.tx_changes_after
        )

    def __repr__(self):
        out = [
            f"tx_changes_before={self.tx_changes_before}",
            f"operations={self.operations}",
            f"tx_changes_after={self.tx_changes_after}",
        ]
        return f"<TransactionMetaV2 [{', '.join(out)}]>"
