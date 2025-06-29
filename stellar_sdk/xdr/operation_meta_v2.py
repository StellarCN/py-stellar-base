# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

from .contract_event import ContractEvent
from .extension_point import ExtensionPoint
from .ledger_entry_changes import LedgerEntryChanges

__all__ = ["OperationMetaV2"]


class OperationMetaV2:
    """
    XDR Source Code::

        struct OperationMetaV2
        {
            ExtensionPoint ext;

            LedgerEntryChanges changes;

            ContractEvent events<>;
        };
    """

    def __init__(
        self,
        ext: ExtensionPoint,
        changes: LedgerEntryChanges,
        events: List[ContractEvent],
    ) -> None:
        _expect_max_length = 4294967295
        if events and len(events) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `events` should be {_expect_max_length}, but got {len(events)}."
            )
        self.ext = ext
        self.changes = changes
        self.events = events

    def pack(self, packer: Packer) -> None:
        self.ext.pack(packer)
        self.changes.pack(packer)
        packer.pack_uint(len(self.events))
        for events_item in self.events:
            events_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> OperationMetaV2:
        ext = ExtensionPoint.unpack(unpacker)
        changes = LedgerEntryChanges.unpack(unpacker)
        length = unpacker.unpack_uint()
        events = []
        for _ in range(length):
            events.append(ContractEvent.unpack(unpacker))
        return cls(
            ext=ext,
            changes=changes,
            events=events,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> OperationMetaV2:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> OperationMetaV2:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.ext,
                self.changes,
                self.events,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ext == other.ext
            and self.changes == other.changes
            and self.events == other.events
        )

    def __repr__(self):
        out = [
            f"ext={self.ext}",
            f"changes={self.changes}",
            f"events={self.events}",
        ]
        return f"<OperationMetaV2 [{', '.join(out)}]>"
