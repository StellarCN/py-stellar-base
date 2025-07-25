# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import Optional

from xdrlib3 import Packer, Unpacker

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

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> LedgerEntryChange:
        type = LedgerEntryChangeType.unpack(unpacker)
        if type == LedgerEntryChangeType.LEDGER_ENTRY_CREATED:
            created = LedgerEntry.unpack(unpacker)
            return cls(type=type, created=created)
        if type == LedgerEntryChangeType.LEDGER_ENTRY_UPDATED:
            updated = LedgerEntry.unpack(unpacker)
            return cls(type=type, updated=updated)
        if type == LedgerEntryChangeType.LEDGER_ENTRY_REMOVED:
            removed = LedgerKey.unpack(unpacker)
            return cls(type=type, removed=removed)
        if type == LedgerEntryChangeType.LEDGER_ENTRY_STATE:
            state = LedgerEntry.unpack(unpacker)
            return cls(type=type, state=state)
        if type == LedgerEntryChangeType.LEDGER_ENTRY_RESTORED:
            restored = LedgerEntry.unpack(unpacker)
            return cls(type=type, restored=restored)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerEntryChange:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LedgerEntryChange:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
        out.append(f"created={self.created}") if self.created is not None else None
        out.append(f"updated={self.updated}") if self.updated is not None else None
        out.append(f"removed={self.removed}") if self.removed is not None else None
        out.append(f"state={self.state}") if self.state is not None else None
        out.append(f"restored={self.restored}") if self.restored is not None else None
        return f"<LedgerEntryChange [{', '.join(out)}]>"
