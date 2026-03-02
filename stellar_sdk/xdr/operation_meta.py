# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .ledger_entry_changes import LedgerEntryChanges

__all__ = ["OperationMeta"]


class OperationMeta:
    """
    XDR Source Code::

        struct OperationMeta
        {
            LedgerEntryChanges changes;
        };
    """

    def __init__(
        self,
        changes: LedgerEntryChanges,
    ) -> None:
        self.changes = changes

    def pack(self, packer: Packer) -> None:
        self.changes.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> OperationMeta:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        changes = LedgerEntryChanges.unpack(unpacker, depth_limit - 1)
        return cls(
            changes=changes,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> OperationMeta:
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
    def from_xdr(cls, xdr: str) -> OperationMeta:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> OperationMeta:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "changes": self.changes.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> OperationMeta:
        changes = LedgerEntryChanges.from_json_dict(json_dict["changes"])
        return cls(
            changes=changes,
        )

    def __hash__(self):
        return hash((self.changes,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.changes == other.changes

    def __repr__(self):
        out = [
            f"changes={self.changes}",
        ]
        return f"<OperationMeta [{', '.join(out)}]>"
