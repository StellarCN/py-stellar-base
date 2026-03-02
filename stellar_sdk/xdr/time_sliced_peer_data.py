# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .peer_stats import PeerStats
from .uint32 import Uint32

__all__ = ["TimeSlicedPeerData"]


class TimeSlicedPeerData:
    """
    XDR Source Code::

        struct TimeSlicedPeerData
        {
            PeerStats peerStats;
            uint32 averageLatencyMs;
        };
    """

    def __init__(
        self,
        peer_stats: PeerStats,
        average_latency_ms: Uint32,
    ) -> None:
        self.peer_stats = peer_stats
        self.average_latency_ms = average_latency_ms

    def pack(self, packer: Packer) -> None:
        self.peer_stats.pack(packer)
        self.average_latency_ms.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> TimeSlicedPeerData:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        peer_stats = PeerStats.unpack(unpacker, depth_limit - 1)
        average_latency_ms = Uint32.unpack(unpacker, depth_limit - 1)
        return cls(
            peer_stats=peer_stats,
            average_latency_ms=average_latency_ms,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TimeSlicedPeerData:
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
    def from_xdr(cls, xdr: str) -> TimeSlicedPeerData:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TimeSlicedPeerData:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "peer_stats": self.peer_stats.to_json_dict(),
            "average_latency_ms": self.average_latency_ms.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> TimeSlicedPeerData:
        peer_stats = PeerStats.from_json_dict(json_dict["peer_stats"])
        average_latency_ms = Uint32.from_json_dict(json_dict["average_latency_ms"])
        return cls(
            peer_stats=peer_stats,
            average_latency_ms=average_latency_ms,
        )

    def __hash__(self):
        return hash(
            (
                self.peer_stats,
                self.average_latency_ms,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.peer_stats == other.peer_stats
            and self.average_latency_ms == other.average_latency_ms
        )

    def __repr__(self):
        out = [
            f"peer_stats={self.peer_stats}",
            f"average_latency_ms={self.average_latency_ms}",
        ]
        return f"<TimeSlicedPeerData [{', '.join(out)}]>"
