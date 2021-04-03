# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .base import *

__all__ = ["Auth"]


class Auth:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct Auth
    {
        // Empty message, just to confirm
        // establishment of MAC keys.
        int unused;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        unused: int,
    ) -> None:
        self.unused = unused

    def pack(self, packer: Packer) -> None:
        Integer(self.unused).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Auth":
        unused = Integer.unpack(unpacker)
        return cls(
            unused=unused,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "Auth":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Auth":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.unused == other.unused

    def __str__(self):
        out = [
            f"unused={self.unused}",
        ]
        return f"<Auth {[', '.join(out)]}>"
