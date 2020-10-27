# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .int32 import Int32

__all__ = ["Price"]


class Price:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct Price
    {
        int32 n; // numerator
        int32 d; // denominator
    };
    ----------------------------------------------------------------
    """

    def __init__(self, n: Int32, d: Int32,) -> None:
        self.n = n
        self.d = d

    def pack(self, packer: Packer) -> None:
        self.n.pack(packer)
        self.d.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Price":
        n = Int32.unpack(unpacker)
        d = Int32.unpack(unpacker)
        return cls(n=n, d=d,)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "Price":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Price":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.n == other.n and self.d == other.d

    def __str__(self):
        out = [
            f"n={self.n}",
            f"d={self.d}",
        ]
        return f"<Price {[', '.join(out)]}>"
