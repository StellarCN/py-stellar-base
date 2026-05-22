# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_LEDGER_ENTRY_CHANGE_TYPE_MAP = {
    0: "created",
    1: "updated",
    2: "removed",
    3: "state",
    4: "restored",
}
_LEDGER_ENTRY_CHANGE_TYPE_REVERSE_MAP = {
    "created": 0,
    "updated": 1,
    "removed": 2,
    "state": 3,
    "restored": 4,
}
__all__ = ["LedgerEntryChangeType"]


class LedgerEntryChangeType(IntEnum):
    """
    XDR Source Code::

        enum LedgerEntryChangeType
        {
            LEDGER_ENTRY_CREATED = 0, // entry was added to the ledger
            LEDGER_ENTRY_UPDATED = 1, // entry was modified in the ledger
            LEDGER_ENTRY_REMOVED = 2, // entry was removed from the ledger
            LEDGER_ENTRY_STATE    = 3, // value of the entry
            LEDGER_ENTRY_RESTORED = 4  // archived entry was restored in the ledger
        };
    """

    LEDGER_ENTRY_CREATED = 0
    LEDGER_ENTRY_UPDATED = 1
    LEDGER_ENTRY_REMOVED = 2
    LEDGER_ENTRY_STATE = 3
    LEDGER_ENTRY_RESTORED = 4

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> LedgerEntryChangeType:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerEntryChangeType:
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
    def from_xdr(cls, xdr: str) -> LedgerEntryChangeType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LedgerEntryChangeType:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _LEDGER_ENTRY_CHANGE_TYPE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> LedgerEntryChangeType:
        return cls(_LEDGER_ENTRY_CHANGE_TYPE_REVERSE_MAP[json_value])
