# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

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
    def unpack(cls, unpacker: Unpacker) -> SorobanAuthorizationEntries:
        length = unpacker.unpack_uint()
        soroban_authorization_entries = []
        for _ in range(length):
            soroban_authorization_entries.append(
                SorobanAuthorizationEntry.unpack(unpacker)
            )
        return cls(soroban_authorization_entries)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SorobanAuthorizationEntries:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SorobanAuthorizationEntries:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(self.soroban_authorization_entries)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.soroban_authorization_entries == other.soroban_authorization_entries

    def __repr__(self):
        return f"<SorobanAuthorizationEntries [soroban_authorization_entries={self.soroban_authorization_entries}]>"
