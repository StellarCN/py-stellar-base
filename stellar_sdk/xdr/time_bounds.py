# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .time_point import TimePoint

__all__ = ["TimeBounds"]


class TimeBounds:
    """
    XDR Source Code::

        struct TimeBounds
        {
            TimePoint minTime;
            TimePoint maxTime; // 0 here means no maxTime
        };
    """

    def __init__(
        self,
        min_time: TimePoint,
        max_time: TimePoint,
    ) -> None:
        self.min_time = min_time
        self.max_time = max_time

    def pack(self, packer: Packer) -> None:
        self.min_time.pack(packer)
        self.max_time.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> TimeBounds:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        min_time = TimePoint.unpack(unpacker, depth_limit - 1)
        max_time = TimePoint.unpack(unpacker, depth_limit - 1)
        return cls(
            min_time=min_time,
            max_time=max_time,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TimeBounds:
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
    def from_xdr(cls, xdr: str) -> TimeBounds:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TimeBounds:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "min_time": self.min_time.to_json_dict(),
            "max_time": self.max_time.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> TimeBounds:
        min_time = TimePoint.from_json_dict(json_dict["min_time"])
        max_time = TimePoint.from_json_dict(json_dict["max_time"])
        return cls(
            min_time=min_time,
            max_time=max_time,
        )

    def __hash__(self):
        return hash(
            (
                self.min_time,
                self.max_time,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.min_time == other.min_time and self.max_time == other.max_time

    def __repr__(self):
        out = [
            f"min_time={self.min_time}",
            f"max_time={self.max_time}",
        ]
        return f"<TimeBounds [{', '.join(out)}]>"
