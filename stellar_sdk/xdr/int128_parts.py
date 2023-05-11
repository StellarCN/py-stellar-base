# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib3 import Packer, Unpacker

from .uint64 import Uint64

__all__ = ["Int128Parts"]


class Int128Parts:
    """
    XDR Source Code::

        struct Int128Parts {
            // Both signed and unsigned 128-bit ints
            // are transported in a pair of uint64s
            // to reduce the risk of sign-extension.
            uint64 lo;
            uint64 hi;
        };
    """

    def __init__(
        self,
        lo: Uint64,
        hi: Uint64,
    ) -> None:
        self.lo = lo
        self.hi = hi

    def pack(self, packer: Packer) -> None:
        self.lo.pack(packer)
        self.hi.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Int128Parts":
        lo = Uint64.unpack(unpacker)
        hi = Uint64.unpack(unpacker)
        return cls(
            lo=lo,
            hi=hi,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "Int128Parts":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Int128Parts":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.lo == other.lo and self.hi == other.hi

    def __str__(self):
        out = [
            f"lo={self.lo}",
            f"hi={self.hi}",
        ]
        return f"<Int128Parts [{', '.join(out)}]>"
