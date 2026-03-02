# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> OperationMetaV2:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        ext = ExtensionPoint.unpack(unpacker, depth_limit - 1)
        changes = LedgerEntryChanges.unpack(unpacker, depth_limit - 1)
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"events length {length} exceeds remaining input length {_remaining}"
            )
        events = []
        for _ in range(length):
            events.append(ContractEvent.unpack(unpacker, depth_limit - 1))
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> OperationMetaV2:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> OperationMetaV2:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "ext": self.ext.to_json_dict(),
            "changes": self.changes.to_json_dict(),
            "events": [item.to_json_dict() for item in self.events],
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> OperationMetaV2:
        ext = ExtensionPoint.from_json_dict(json_dict["ext"])
        changes = LedgerEntryChanges.from_json_dict(json_dict["changes"])
        events = [ContractEvent.from_json_dict(item) for item in json_dict["events"]]
        return cls(
            ext=ext,
            changes=changes,
            events=events,
        )

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
