# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .soroban_authorization_entry import SorobanAuthorizationEntry

__all__ = ["SorobanAuthorizationEntries"]


class SorobanAuthorizationEntries:
    """
    XDR Source Code::

        typedef SorobanAuthorizationEntry SorobanAuthorizationEntries<>;
    """

    def __init__(
        self, soroban_authorization_entries: List[SorobanAuthorizationEntry]
    ) -> None:
        _expect_max_length = 4294967295
        if (
            soroban_authorization_entries
            and len(soroban_authorization_entries) > _expect_max_length
        ):
            raise ValueError(
                f"The maximum length of `soroban_authorization_entries` should be {_expect_max_length}, but got {len(soroban_authorization_entries)}."
            )
        self.soroban_authorization_entries = soroban_authorization_entries

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.soroban_authorization_entries))
        for soroban_authorization_entries_item in self.soroban_authorization_entries:
            soroban_authorization_entries_item.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SorobanAuthorizationEntries:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"soroban_authorization_entries length {length} exceeds remaining input length {_remaining}"
            )
        soroban_authorization_entries = []
        for _ in range(length):
            soroban_authorization_entries.append(
                SorobanAuthorizationEntry.unpack(unpacker, depth_limit - 1)
            )
        return cls(soroban_authorization_entries)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SorobanAuthorizationEntries:
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
    def from_xdr(cls, xdr: str) -> SorobanAuthorizationEntries:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SorobanAuthorizationEntries:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        return [item.to_json_dict() for item in self.soroban_authorization_entries]

    @classmethod
    def from_json_dict(cls, json_value: list) -> SorobanAuthorizationEntries:
        return cls(
            [SorobanAuthorizationEntry.from_json_dict(item) for item in json_value]
        )

    def __hash__(self):
        return hash((self.soroban_authorization_entries,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.soroban_authorization_entries == other.soroban_authorization_entries

    def __repr__(self):
        return f"<SorobanAuthorizationEntries [soroban_authorization_entries={self.soroban_authorization_entries}]>"
