# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .base import Opaque

__all__ = ["Thresholds"]


class Thresholds:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef opaque Thresholds[4];
    ----------------------------------------------------------------
    """

    def __init__(self, thresholds: bytes) -> None:
        self.thresholds = thresholds

    def pack(self, packer: Packer) -> None:
        Opaque(self.thresholds, 4, True).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Thresholds":
        thresholds = Opaque.unpack(unpacker, 4, True)
        return cls(thresholds)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "Thresholds":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Thresholds":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.thresholds == other.thresholds

    def __str__(self):
        return f"<Thresholds [thresholds={self.thresholds}]>"
