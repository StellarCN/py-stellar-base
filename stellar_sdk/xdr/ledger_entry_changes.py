# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

from .ledger_entry_change import LedgerEntryChange

__all__ = ["LedgerEntryChanges"]


class LedgerEntryChanges:
    """
    XDR Source Code::

        typedef LedgerEntryChange LedgerEntryChanges<>;
    """

    def __init__(self, ledger_entry_changes: List[LedgerEntryChange]) -> None:
        _expect_max_length = 4294967295
        if ledger_entry_changes and len(ledger_entry_changes) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `ledger_entry_changes` should be {_expect_max_length}, but got {len(ledger_entry_changes)}."
            )
        self.ledger_entry_changes = ledger_entry_changes

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.ledger_entry_changes))
        for ledger_entry_changes_item in self.ledger_entry_changes:
            ledger_entry_changes_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> LedgerEntryChanges:
        length = unpacker.unpack_uint()
        ledger_entry_changes = []
        for _ in range(length):
            ledger_entry_changes.append(LedgerEntryChange.unpack(unpacker))
        return cls(ledger_entry_changes)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerEntryChanges:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LedgerEntryChanges:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(self.ledger_entry_changes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.ledger_entry_changes == other.ledger_entry_changes

    def __repr__(self):
        return (
            f"<LedgerEntryChanges [ledger_entry_changes={self.ledger_entry_changes}]>"
        )
