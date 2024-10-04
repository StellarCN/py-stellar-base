# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

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
    def unpack(cls, unpacker: Unpacker) -> TimeSlicedPeerData:
        peer_stats = PeerStats.unpack(unpacker)
        average_latency_ms = Uint32.unpack(unpacker)
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
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> TimeSlicedPeerData:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
