# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> LedgerEntryChanges:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"ledger_entry_changes length {length} exceeds remaining input length {_remaining}"
            )
        ledger_entry_changes = []
        for _ in range(length):
            ledger_entry_changes.append(
                LedgerEntryChange.unpack(unpacker, depth_limit - 1)
            )
        return cls(ledger_entry_changes)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerEntryChanges:
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
    def from_xdr(cls, xdr: str) -> LedgerEntryChanges:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LedgerEntryChanges:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        return [item.to_json_dict() for item in self.ledger_entry_changes]

    @classmethod
    def from_json_dict(cls, json_value: list) -> LedgerEntryChanges:
        return cls([LedgerEntryChange.from_json_dict(item) for item in json_value])

    def __hash__(self):
        return hash((self.ledger_entry_changes,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.ledger_entry_changes == other.ledger_entry_changes

    def __repr__(self):
        return (
            f"<LedgerEntryChanges [ledger_entry_changes={self.ledger_entry_changes}]>"
        )
