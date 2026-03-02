# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .ledger_entry import LedgerEntry
from .ledger_entry_change_type import LedgerEntryChangeType
from .ledger_key import LedgerKey

__all__ = ["LedgerEntryChange"]


class LedgerEntryChange:
    """
    XDR Source Code::

        union LedgerEntryChange switch (LedgerEntryChangeType type)
        {
        case LEDGER_ENTRY_CREATED:
            LedgerEntry created;
        case LEDGER_ENTRY_UPDATED:
            LedgerEntry updated;
        case LEDGER_ENTRY_REMOVED:
            LedgerKey removed;
        case LEDGER_ENTRY_STATE:
            LedgerEntry state;
        case LEDGER_ENTRY_RESTORED:
            LedgerEntry restored;
        };
    """

    def __init__(
        self,
        type: LedgerEntryChangeType,
        created: Optional[LedgerEntry] = None,
        updated: Optional[LedgerEntry] = None,
        removed: Optional[LedgerKey] = None,
        state: Optional[LedgerEntry] = None,
        restored: Optional[LedgerEntry] = None,
    ) -> None:
        self.type = type
        self.created = created
        self.updated = updated
        self.removed = removed
        self.state = state
        self.restored = restored

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == LedgerEntryChangeType.LEDGER_ENTRY_CREATED:
            if self.created is None:
                raise ValueError("created should not be None.")
            self.created.pack(packer)
            return
        if self.type == LedgerEntryChangeType.LEDGER_ENTRY_UPDATED:
            if self.updated is None:
                raise ValueError("updated should not be None.")
            self.updated.pack(packer)
            return
        if self.type == LedgerEntryChangeType.LEDGER_ENTRY_REMOVED:
            if self.removed is None:
                raise ValueError("removed should not be None.")
            self.removed.pack(packer)
            return
        if self.type == LedgerEntryChangeType.LEDGER_ENTRY_STATE:
            if self.state is None:
                raise ValueError("state should not be None.")
            self.state.pack(packer)
            return
        if self.type == LedgerEntryChangeType.LEDGER_ENTRY_RESTORED:
            if self.restored is None:
                raise ValueError("restored should not be None.")
            self.restored.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> LedgerEntryChange:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = LedgerEntryChangeType.unpack(unpacker)
        if type == LedgerEntryChangeType.LEDGER_ENTRY_CREATED:
            created = LedgerEntry.unpack(unpacker, depth_limit - 1)
            return cls(type=type, created=created)
        if type == LedgerEntryChangeType.LEDGER_ENTRY_UPDATED:
            updated = LedgerEntry.unpack(unpacker, depth_limit - 1)
            return cls(type=type, updated=updated)
        if type == LedgerEntryChangeType.LEDGER_ENTRY_REMOVED:
            removed = LedgerKey.unpack(unpacker, depth_limit - 1)
            return cls(type=type, removed=removed)
        if type == LedgerEntryChangeType.LEDGER_ENTRY_STATE:
            state = LedgerEntry.unpack(unpacker, depth_limit - 1)
            return cls(type=type, state=state)
        if type == LedgerEntryChangeType.LEDGER_ENTRY_RESTORED:
            restored = LedgerEntry.unpack(unpacker, depth_limit - 1)
            return cls(type=type, restored=restored)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerEntryChange:
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
    def from_xdr(cls, xdr: str) -> LedgerEntryChange:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LedgerEntryChange:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.type == LedgerEntryChangeType.LEDGER_ENTRY_CREATED:
            assert self.created is not None
            return {"created": self.created.to_json_dict()}
        if self.type == LedgerEntryChangeType.LEDGER_ENTRY_UPDATED:
            assert self.updated is not None
            return {"updated": self.updated.to_json_dict()}
        if self.type == LedgerEntryChangeType.LEDGER_ENTRY_REMOVED:
            assert self.removed is not None
            return {"removed": self.removed.to_json_dict()}
        if self.type == LedgerEntryChangeType.LEDGER_ENTRY_STATE:
            assert self.state is not None
            return {"state": self.state.to_json_dict()}
        if self.type == LedgerEntryChangeType.LEDGER_ENTRY_RESTORED:
            assert self.restored is not None
            return {"restored": self.restored.to_json_dict()}
        raise ValueError(f"Unknown type in LedgerEntryChange: {self.type}")

    @classmethod
    def from_json_dict(cls, json_value: dict) -> LedgerEntryChange:
        if len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for LedgerEntryChange, got: {json_value}"
            )
        key = next(iter(json_value))
        type = LedgerEntryChangeType.from_json_dict(key)
        if key == "created":
            created = LedgerEntry.from_json_dict(json_value["created"])
            return cls(type=type, created=created)
        if key == "updated":
            updated = LedgerEntry.from_json_dict(json_value["updated"])
            return cls(type=type, updated=updated)
        if key == "removed":
            removed = LedgerKey.from_json_dict(json_value["removed"])
            return cls(type=type, removed=removed)
        if key == "state":
            state = LedgerEntry.from_json_dict(json_value["state"])
            return cls(type=type, state=state)
        if key == "restored":
            restored = LedgerEntry.from_json_dict(json_value["restored"])
            return cls(type=type, restored=restored)
        raise ValueError(f"Unknown key '{key}' for LedgerEntryChange")

    def __hash__(self):
        return hash(
            (
                self.type,
                self.created,
                self.updated,
                self.removed,
                self.state,
                self.restored,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.created == other.created
            and self.updated == other.updated
            and self.removed == other.removed
            and self.state == other.state
            and self.restored == other.restored
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        if self.created is not None:
            out.append(f"created={self.created}")
        if self.updated is not None:
            out.append(f"updated={self.updated}")
        if self.removed is not None:
            out.append(f"removed={self.removed}")
        if self.state is not None:
            out.append(f"state={self.state}")
        if self.restored is not None:
            out.append(f"restored={self.restored}")
        return f"<LedgerEntryChange [{', '.join(out)}]>"
