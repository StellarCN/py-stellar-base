# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

from .config_setting_entry import ConfigSettingEntry

__all__ = ["ConfigUpgradeSet"]


class ConfigUpgradeSet:
    """
    XDR Source Code::

        struct ConfigUpgradeSet {
            ConfigSettingEntry updatedEntry<>;
        };
    """

    def __init__(
        self,
        updated_entry: List[ConfigSettingEntry],
    ) -> None:
        _expect_max_length = 4294967295
        if updated_entry and len(updated_entry) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `updated_entry` should be {_expect_max_length}, but got {len(updated_entry)}."
            )
        self.updated_entry = updated_entry

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.updated_entry))
        for updated_entry_item in self.updated_entry:
            updated_entry_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ConfigUpgradeSet:
        length = unpacker.unpack_uint()
        updated_entry = []
        for _ in range(length):
            updated_entry.append(ConfigSettingEntry.unpack(unpacker))
        return cls(
            updated_entry=updated_entry,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ConfigUpgradeSet:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ConfigUpgradeSet:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash((self.updated_entry,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.updated_entry == other.updated_entry

    def __repr__(self):
        out = [
            f"updated_entry={self.updated_entry}",
        ]
        return f"<ConfigUpgradeSet [{', '.join(out)}]>"
