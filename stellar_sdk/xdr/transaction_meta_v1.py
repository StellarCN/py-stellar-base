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

__all__ = ["TransactionMetaV1"]


class TransactionMetaV1:
    """
    XDR Source Code::

        struct TransactionMetaV1
        {
            LedgerEntryChanges txChanges; // tx level changes if any
            OperationMeta operations<>;   // meta for each operation
        };
    """

    def __init__(
        self,
        tx_changes: LedgerEntryChanges,
        operations: List[OperationMeta],
    ) -> None:
        _expect_max_length = 4294967295
        if operations and len(operations) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `operations` should be {_expect_max_length}, but got {len(operations)}."
            )
        self.tx_changes = tx_changes
        self.operations = operations

    def pack(self, packer: Packer) -> None:
        self.tx_changes.pack(packer)
        packer.pack_uint(len(self.operations))
        for operations_item in self.operations:
            operations_item.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> TransactionMetaV1:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        tx_changes = LedgerEntryChanges.unpack(unpacker, depth_limit - 1)
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"operations length {length} exceeds remaining input length {_remaining}"
            )
        operations = []
        for _ in range(length):
            operations.append(OperationMeta.unpack(unpacker, depth_limit - 1))
        return cls(
            tx_changes=tx_changes,
            operations=operations,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TransactionMetaV1:
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
    def from_xdr(cls, xdr: str) -> TransactionMetaV1:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TransactionMetaV1:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "tx_changes": self.tx_changes.to_json_dict(),
            "operations": [item.to_json_dict() for item in self.operations],
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> TransactionMetaV1:
        tx_changes = LedgerEntryChanges.from_json_dict(json_dict["tx_changes"])
        operations = [
            OperationMeta.from_json_dict(item) for item in json_dict["operations"]
        ]
        return cls(
            tx_changes=tx_changes,
            operations=operations,
        )

    def __hash__(self):
        return hash(
            (
                self.tx_changes,
                self.operations,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.tx_changes == other.tx_changes and self.operations == other.operations
        )

    def __repr__(self):
        out = [
            f"tx_changes={self.tx_changes}",
            f"operations={self.operations}",
        ]
        return f"<TransactionMetaV1 [{', '.join(out)}]>"
