# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .ledger_key import LedgerKey
from .uint32 import Uint32

__all__ = ["ColdArchiveDeletedLeaf"]


class ColdArchiveDeletedLeaf:
    """
    XDR Source Code::

        struct ColdArchiveDeletedLeaf
        {
            uint32 index;
            LedgerKey deletedKey;
        };
    """

    def __init__(
        self,
        index: Uint32,
        deleted_key: LedgerKey,
    ) -> None:
        self.index = index
        self.deleted_key = deleted_key

    def pack(self, packer: Packer) -> None:
        self.index.pack(packer)
        self.deleted_key.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ColdArchiveDeletedLeaf:
        index = Uint32.unpack(unpacker)
        deleted_key = LedgerKey.unpack(unpacker)
        return cls(
            index=index,
            deleted_key=deleted_key,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ColdArchiveDeletedLeaf:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ColdArchiveDeletedLeaf:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.index,
                self.deleted_key,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.index == other.index and self.deleted_key == other.deleted_key

    def __repr__(self):
        out = [
            f"index={self.index}",
            f"deleted_key={self.deleted_key}",
        ]
        return f"<ColdArchiveDeletedLeaf [{', '.join(out)}]>"
