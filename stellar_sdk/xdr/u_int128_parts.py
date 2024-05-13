# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .uint64 import Uint64

__all__ = ["UInt128Parts"]


class UInt128Parts:
    """
    XDR Source Code::

        struct UInt128Parts {
            uint64 hi;
            uint64 lo;
        };
    """

    def __init__(
        self,
        hi: Uint64,
        lo: Uint64,
    ) -> None:
        self.hi = hi
        self.lo = lo

    def pack(self, packer: Packer) -> None:
        self.hi.pack(packer)
        self.lo.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> UInt128Parts:
        hi = Uint64.unpack(unpacker)
        lo = Uint64.unpack(unpacker)
        return cls(
            hi=hi,
            lo=lo,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> UInt128Parts:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> UInt128Parts:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.hi,
                self.lo,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.hi == other.hi and self.lo == other.lo

    def __repr__(self):
        out = [
            f"hi={self.hi}",
            f"lo={self.lo}",
        ]
        return f"<UInt128Parts [{', '.join(out)}]>"
