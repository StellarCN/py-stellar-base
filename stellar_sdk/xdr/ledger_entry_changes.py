# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib import Packer, Unpacker

from ..exceptions import ValueError
from .ledger_entry_change import LedgerEntryChange

__all__ = ["LedgerEntryChanges"]


class LedgerEntryChanges:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef LedgerEntryChange LedgerEntryChanges<>;
    ----------------------------------------------------------------
    """

    def __init__(self, ledger_entry_changes: List[LedgerEntryChange]) -> None:
        if ledger_entry_changes and len(ledger_entry_changes) > 4294967295:
            raise ValueError(
                f"The maximum length of `ledger_entry_changes` should be 4294967295, but got {len(ledger_entry_changes)}."
            )
        self.ledger_entry_changes = ledger_entry_changes

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.ledger_entry_changes))
        for ledger_entry_change in self.ledger_entry_changes:
            ledger_entry_change.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerEntryChanges":
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
    def from_xdr_bytes(cls, xdr: bytes) -> "LedgerEntryChanges":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerEntryChanges":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.ledger_entry_changes == other.ledger_entry_changes

    def __str__(self):
        return (
            f"<LedgerEntryChanges [ledger_entry_changes={self.ledger_entry_changes}]>"
        )
