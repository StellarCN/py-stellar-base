# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .base import Boolean
from .uint32 import Uint32

__all__ = ["ColdArchiveBoundaryLeaf"]


class ColdArchiveBoundaryLeaf:
    """
    XDR Source Code::

        struct ColdArchiveBoundaryLeaf
        {
            uint32 index;
            bool isLowerBound;
        };
    """

    def __init__(
        self,
        index: Uint32,
        is_lower_bound: bool,
    ) -> None:
        self.index = index
        self.is_lower_bound = is_lower_bound

    def pack(self, packer: Packer) -> None:
        self.index.pack(packer)
        Boolean(self.is_lower_bound).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ColdArchiveBoundaryLeaf:
        index = Uint32.unpack(unpacker)
        is_lower_bound = Boolean.unpack(unpacker)
        return cls(
            index=index,
            is_lower_bound=is_lower_bound,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ColdArchiveBoundaryLeaf:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ColdArchiveBoundaryLeaf:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.index,
                self.is_lower_bound,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.index == other.index and self.is_lower_bound == other.is_lower_bound

    def __repr__(self):
        out = [
            f"index={self.index}",
            f"is_lower_bound={self.is_lower_bound}",
        ]
        return f"<ColdArchiveBoundaryLeaf [{', '.join(out)}]>"
