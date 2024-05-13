# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .base import Opaque

__all__ = ["Hash"]


class Hash:
    """
    XDR Source Code::

        typedef opaque Hash[32];
    """

    def __init__(self, hash: bytes) -> None:
        self.hash = hash

    def pack(self, packer: Packer) -> None:
        Opaque(self.hash, 32, True).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> Hash:
        hash = Opaque.unpack(unpacker, 32, True)
        return cls(hash)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Hash:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> Hash:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(self.hash)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.hash == other.hash

    def __repr__(self):
        return f"<Hash [hash={self.hash}]>"
