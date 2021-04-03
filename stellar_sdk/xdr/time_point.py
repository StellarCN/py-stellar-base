# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .uint64 import Uint64

__all__ = ["TimePoint"]


class TimePoint:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef uint64 TimePoint;
    ----------------------------------------------------------------
    """

    def __init__(self, time_point: Uint64) -> None:

        self.time_point = time_point

    def pack(self, packer: Packer) -> None:
        self.time_point.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TimePoint":
        time_point = Uint64.unpack(unpacker)
        return cls(time_point)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "TimePoint":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TimePoint":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.time_point == other.time_point

    def __str__(self):
        return f"<TimePoint [time_point={self.time_point}]>"
