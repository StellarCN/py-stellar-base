# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ConfigUpgradeSet:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"updated_entry length {length} exceeds remaining input length {_remaining}"
            )
        updated_entry = []
        for _ in range(length):
            updated_entry.append(ConfigSettingEntry.unpack(unpacker, depth_limit - 1))
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ConfigUpgradeSet:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ConfigUpgradeSet:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "updated_entry": [item.to_json_dict() for item in self.updated_entry],
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> ConfigUpgradeSet:
        updated_entry = [
            ConfigSettingEntry.from_json_dict(item)
            for item in json_dict["updated_entry"]
        ]
        return cls(
            updated_entry=updated_entry,
        )

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
