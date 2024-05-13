# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .uint64 import Uint64

__all__ = ["UInt256Parts"]


class UInt256Parts:
    """
    XDR Source Code::

        struct UInt256Parts {
            uint64 hi_hi;
            uint64 hi_lo;
            uint64 lo_hi;
            uint64 lo_lo;
        };
    """

    def __init__(
        self,
        hi_hi: Uint64,
        hi_lo: Uint64,
        lo_hi: Uint64,
        lo_lo: Uint64,
    ) -> None:
        self.hi_hi = hi_hi
        self.hi_lo = hi_lo
        self.lo_hi = lo_hi
        self.lo_lo = lo_lo

    def pack(self, packer: Packer) -> None:
        self.hi_hi.pack(packer)
        self.hi_lo.pack(packer)
        self.lo_hi.pack(packer)
        self.lo_lo.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> UInt256Parts:
        hi_hi = Uint64.unpack(unpacker)
        hi_lo = Uint64.unpack(unpacker)
        lo_hi = Uint64.unpack(unpacker)
        lo_lo = Uint64.unpack(unpacker)
        return cls(
            hi_hi=hi_hi,
            hi_lo=hi_lo,
            lo_hi=lo_hi,
            lo_lo=lo_lo,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> UInt256Parts:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> UInt256Parts:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.hi_hi,
                self.hi_lo,
                self.lo_hi,
                self.lo_lo,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.hi_hi == other.hi_hi
            and self.hi_lo == other.hi_lo
            and self.lo_hi == other.lo_hi
            and self.lo_lo == other.lo_lo
        )

    def __repr__(self):
        out = [
            f"hi_hi={self.hi_hi}",
            f"hi_lo={self.hi_lo}",
            f"lo_hi={self.lo_hi}",
            f"lo_lo={self.lo_lo}",
        ]
        return f"<UInt256Parts [{', '.join(out)}]>"
