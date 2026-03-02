# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .uint64 import Uint64

__all__ = ["TimePoint"]


class TimePoint:
    """
    XDR Source Code::

        typedef uint64 TimePoint;
    """

    def __init__(self, time_point: Uint64) -> None:
        self.time_point = time_point

    def pack(self, packer: Packer) -> None:
        self.time_point.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> TimePoint:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        time_point = Uint64.unpack(unpacker, depth_limit - 1)
        return cls(time_point)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TimePoint:
        unpacker = Unpacker(xdr)
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> TimePoint:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TimePoint:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        return self.time_point.to_json_dict()

    @classmethod
    def from_json_dict(cls, json_value: str) -> TimePoint:
        return cls(Uint64.from_json_dict(json_value))

    def __hash__(self):
        return hash((self.time_point,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.time_point == other.time_point

    def __repr__(self):
        return f"<TimePoint [time_point={self.time_point}]>"
