# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .base import Opaque

__all__ = ["ShortHashSeed"]


class ShortHashSeed:
    """
    XDR Source Code::

        struct ShortHashSeed
        {
            opaque seed[16];
        };
    """

    def __init__(
        self,
        seed: bytes,
    ) -> None:
        self.seed = seed

    def pack(self, packer: Packer) -> None:
        Opaque(self.seed, 16, True).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ShortHashSeed:
        seed = Opaque.unpack(unpacker, 16, True)
        return cls(
            seed=seed,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ShortHashSeed:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ShortHashSeed:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash((self.seed,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.seed == other.seed

    def __repr__(self):
        out = [
            f"seed={self.seed}",
        ]
        return f"<ShortHashSeed [{', '.join(out)}]>"
