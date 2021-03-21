# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .base import *

__all__ = ["HmacSha256Mac"]


class HmacSha256Mac:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct HmacSha256Mac
    {
        opaque mac[32];
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        mac: bytes,
    ) -> None:
        self.mac = mac

    def pack(self, packer: Packer) -> None:
        Opaque(self.mac, 32, True).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "HmacSha256Mac":
        mac = Opaque.unpack(unpacker, 32, True)
        return cls(
            mac=mac,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "HmacSha256Mac":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "HmacSha256Mac":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.mac == other.mac

    def __str__(self):
        out = [
            f"mac={self.mac}",
        ]
        return f"<HmacSha256Mac {[', '.join(out)]}>"
