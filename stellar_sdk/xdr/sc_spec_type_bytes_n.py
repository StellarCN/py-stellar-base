# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .uint32 import Uint32

__all__ = ["SCSpecTypeBytesN"]


class SCSpecTypeBytesN:
    """
    XDR Source Code::

        struct SCSpecTypeBytesN
        {
            uint32 n;
        };
    """

    def __init__(
        self,
        n: Uint32,
    ) -> None:
        self.n = n

    def pack(self, packer: Packer) -> None:
        self.n.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCSpecTypeBytesN:
        n = Uint32.unpack(unpacker)
        return cls(
            n=n,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCSpecTypeBytesN:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCSpecTypeBytesN:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash((self.n,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.n == other.n

    def __repr__(self):
        out = [
            f"n={self.n}",
        ]
        return f"<SCSpecTypeBytesN [{', '.join(out)}]>"
