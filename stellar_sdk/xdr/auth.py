# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .base import Integer

__all__ = ["Auth"]


class Auth:
    """
    XDR Source Code::

        struct Auth
        {
            int flags;
        };
    """

    def __init__(
        self,
        flags: int,
    ) -> None:
        self.flags = flags

    def pack(self, packer: Packer) -> None:
        Integer(self.flags).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> Auth:
        flags = Integer.unpack(unpacker)
        return cls(
            flags=flags,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Auth:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> Auth:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash((self.flags,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.flags == other.flags

    def __repr__(self):
        out = [
            f"flags={self.flags}",
        ]
        return f"<Auth [{', '.join(out)}]>"
