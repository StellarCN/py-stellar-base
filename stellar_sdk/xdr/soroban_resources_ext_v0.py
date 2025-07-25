# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

from .uint32 import Uint32

__all__ = ["SorobanResourcesExtV0"]


class SorobanResourcesExtV0:
    """
    XDR Source Code::

        struct SorobanResourcesExtV0
        {
            // Vector of indices representing what Soroban
            // entries in the footprint are archived, based on the
            // order of keys provided in the readWrite footprint.
            uint32 archivedSorobanEntries<>;
        };
    """

    def __init__(
        self,
        archived_soroban_entries: List[Uint32],
    ) -> None:
        _expect_max_length = 4294967295
        if (
            archived_soroban_entries
            and len(archived_soroban_entries) > _expect_max_length
        ):
            raise ValueError(
                f"The maximum length of `archived_soroban_entries` should be {_expect_max_length}, but got {len(archived_soroban_entries)}."
            )
        self.archived_soroban_entries = archived_soroban_entries

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.archived_soroban_entries))
        for archived_soroban_entries_item in self.archived_soroban_entries:
            archived_soroban_entries_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SorobanResourcesExtV0:
        length = unpacker.unpack_uint()
        archived_soroban_entries = []
        for _ in range(length):
            archived_soroban_entries.append(Uint32.unpack(unpacker))
        return cls(
            archived_soroban_entries=archived_soroban_entries,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SorobanResourcesExtV0:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SorobanResourcesExtV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash((self.archived_soroban_entries,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.archived_soroban_entries == other.archived_soroban_entries

    def __repr__(self):
        out = [
            f"archived_soroban_entries={self.archived_soroban_entries}",
        ]
        return f"<SorobanResourcesExtV0 [{', '.join(out)}]>"
