# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .hash import Hash
from .uint32 import Uint32

__all__ = ["ColdArchiveHashEntry"]


class ColdArchiveHashEntry:
    """
    XDR Source Code::

        struct ColdArchiveHashEntry
        {
            uint32 index;
            uint32 level;
            Hash hash;
        };
    """

    def __init__(
        self,
        index: Uint32,
        level: Uint32,
        hash: Hash,
    ) -> None:
        self.index = index
        self.level = level
        self.hash = hash

    def pack(self, packer: Packer) -> None:
        self.index.pack(packer)
        self.level.pack(packer)
        self.hash.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ColdArchiveHashEntry:
        index = Uint32.unpack(unpacker)
        level = Uint32.unpack(unpacker)
        hash = Hash.unpack(unpacker)
        return cls(
            index=index,
            level=level,
            hash=hash,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ColdArchiveHashEntry:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ColdArchiveHashEntry:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.index,
                self.level,
                self.hash,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.index == other.index
            and self.level == other.level
            and self.hash == other.hash
        )

    def __repr__(self):
        out = [
            f"index={self.index}",
            f"level={self.level}",
            f"hash={self.hash}",
        ]
        return f"<ColdArchiveHashEntry [{', '.join(out)}]>"
