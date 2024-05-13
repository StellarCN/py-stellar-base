# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .base import Opaque

__all__ = ["Curve25519Public"]


class Curve25519Public:
    """
    XDR Source Code::

        struct Curve25519Public
        {
            opaque key[32];
        };
    """

    def __init__(
        self,
        key: bytes,
    ) -> None:
        self.key = key

    def pack(self, packer: Packer) -> None:
        Opaque(self.key, 32, True).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> Curve25519Public:
        key = Opaque.unpack(unpacker, 32, True)
        return cls(
            key=key,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Curve25519Public:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> Curve25519Public:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash((self.key,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.key == other.key

    def __repr__(self):
        out = [
            f"key={self.key}",
        ]
        return f"<Curve25519Public [{', '.join(out)}]>"
