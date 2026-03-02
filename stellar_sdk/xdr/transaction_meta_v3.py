# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List, Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> TransactionMetaV3:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        ext = ExtensionPoint.unpack(unpacker, depth_limit - 1)
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
        soroban_meta = (
            SorobanTransactionMeta.unpack(unpacker, depth_limit - 1)
            if unpacker.unpack_uint()
            else None
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> TransactionMetaV3:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TransactionMetaV3:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "ext": self.ext.to_json_dict(),
            "tx_changes_before": self.tx_changes_before.to_json_dict(),
            "operations": [item.to_json_dict() for item in self.operations],
            "tx_changes_after": self.tx_changes_after.to_json_dict(),
            "soroban_meta": (
                self.soroban_meta.to_json_dict()
                if self.soroban_meta is not None
                else None
            ),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> TransactionMetaV3:
        ext = ExtensionPoint.from_json_dict(json_dict["ext"])
        tx_changes_before = LedgerEntryChanges.from_json_dict(
            json_dict["tx_changes_before"]
        )
        operations = [
            OperationMeta.from_json_dict(item) for item in json_dict["operations"]
        ]
        tx_changes_after = LedgerEntryChanges.from_json_dict(
            json_dict["tx_changes_after"]
        )
        soroban_meta = (
            SorobanTransactionMeta.from_json_dict(json_dict["soroban_meta"])
            if json_dict["soroban_meta"] is not None
            else None
        )
        return cls(
            ext=ext,
            tx_changes_before=tx_changes_before,
            operations=operations,
            tx_changes_after=tx_changes_after,
            soroban_meta=soroban_meta,
        )

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
