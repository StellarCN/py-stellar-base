# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .uint64 import Uint64

__all__ = ["Duration"]


class Duration:
    """
    XDR Source Code::

        typedef uint64 Duration;
    """

    def __init__(self, duration: Uint64) -> None:
        self.duration = duration

    def pack(self, packer: Packer) -> None:
        self.duration.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> Duration:
        duration = Uint64.unpack(unpacker)
        return cls(duration)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Duration:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> Duration:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(self.duration)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.duration == other.duration

    def __repr__(self):
        return f"<Duration [duration={self.duration}]>"
