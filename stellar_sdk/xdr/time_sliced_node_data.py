# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .base import Boolean
from .uint32 import Uint32

__all__ = ["TimeSlicedNodeData"]


class TimeSlicedNodeData:
    """
    XDR Source Code::

        struct TimeSlicedNodeData
        {
            uint32 addedAuthenticatedPeers;
            uint32 droppedAuthenticatedPeers;
            uint32 totalInboundPeerCount;
            uint32 totalOutboundPeerCount;

            // SCP stats
            uint32 p75SCPFirstToSelfLatencyMs;
            uint32 p75SCPSelfToOtherLatencyMs;

            // How many times the node lost sync in the time slice
            uint32 lostSyncCount;

            // Config data
            bool isValidator;
            uint32 maxInboundPeerCount;
            uint32 maxOutboundPeerCount;
        };
    """

    def __init__(
        self,
        added_authenticated_peers: Uint32,
        dropped_authenticated_peers: Uint32,
        total_inbound_peer_count: Uint32,
        total_outbound_peer_count: Uint32,
        p75_scp_first_to_self_latency_ms: Uint32,
        p75_scp_self_to_other_latency_ms: Uint32,
        lost_sync_count: Uint32,
        is_validator: bool,
        max_inbound_peer_count: Uint32,
        max_outbound_peer_count: Uint32,
    ) -> None:
        self.added_authenticated_peers = added_authenticated_peers
        self.dropped_authenticated_peers = dropped_authenticated_peers
        self.total_inbound_peer_count = total_inbound_peer_count
        self.total_outbound_peer_count = total_outbound_peer_count
        self.p75_scp_first_to_self_latency_ms = p75_scp_first_to_self_latency_ms
        self.p75_scp_self_to_other_latency_ms = p75_scp_self_to_other_latency_ms
        self.lost_sync_count = lost_sync_count
        self.is_validator = is_validator
        self.max_inbound_peer_count = max_inbound_peer_count
        self.max_outbound_peer_count = max_outbound_peer_count

    def pack(self, packer: Packer) -> None:
        self.added_authenticated_peers.pack(packer)
        self.dropped_authenticated_peers.pack(packer)
        self.total_inbound_peer_count.pack(packer)
        self.total_outbound_peer_count.pack(packer)
        self.p75_scp_first_to_self_latency_ms.pack(packer)
        self.p75_scp_self_to_other_latency_ms.pack(packer)
        self.lost_sync_count.pack(packer)
        Boolean(self.is_validator).pack(packer)
        self.max_inbound_peer_count.pack(packer)
        self.max_outbound_peer_count.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> TimeSlicedNodeData:
        added_authenticated_peers = Uint32.unpack(unpacker)
        dropped_authenticated_peers = Uint32.unpack(unpacker)
        total_inbound_peer_count = Uint32.unpack(unpacker)
        total_outbound_peer_count = Uint32.unpack(unpacker)
        p75_scp_first_to_self_latency_ms = Uint32.unpack(unpacker)
        p75_scp_self_to_other_latency_ms = Uint32.unpack(unpacker)
        lost_sync_count = Uint32.unpack(unpacker)
        is_validator = Boolean.unpack(unpacker)
        max_inbound_peer_count = Uint32.unpack(unpacker)
        max_outbound_peer_count = Uint32.unpack(unpacker)
        return cls(
            added_authenticated_peers=added_authenticated_peers,
            dropped_authenticated_peers=dropped_authenticated_peers,
            total_inbound_peer_count=total_inbound_peer_count,
            total_outbound_peer_count=total_outbound_peer_count,
            p75_scp_first_to_self_latency_ms=p75_scp_first_to_self_latency_ms,
            p75_scp_self_to_other_latency_ms=p75_scp_self_to_other_latency_ms,
            lost_sync_count=lost_sync_count,
            is_validator=is_validator,
            max_inbound_peer_count=max_inbound_peer_count,
            max_outbound_peer_count=max_outbound_peer_count,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TimeSlicedNodeData:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> TimeSlicedNodeData:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.added_authenticated_peers,
                self.dropped_authenticated_peers,
                self.total_inbound_peer_count,
                self.total_outbound_peer_count,
                self.p75_scp_first_to_self_latency_ms,
                self.p75_scp_self_to_other_latency_ms,
                self.lost_sync_count,
                self.is_validator,
                self.max_inbound_peer_count,
                self.max_outbound_peer_count,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.added_authenticated_peers == other.added_authenticated_peers
            and self.dropped_authenticated_peers == other.dropped_authenticated_peers
            and self.total_inbound_peer_count == other.total_inbound_peer_count
            and self.total_outbound_peer_count == other.total_outbound_peer_count
            and self.p75_scp_first_to_self_latency_ms
            == other.p75_scp_first_to_self_latency_ms
            and self.p75_scp_self_to_other_latency_ms
            == other.p75_scp_self_to_other_latency_ms
            and self.lost_sync_count == other.lost_sync_count
            and self.is_validator == other.is_validator
            and self.max_inbound_peer_count == other.max_inbound_peer_count
            and self.max_outbound_peer_count == other.max_outbound_peer_count
        )

    def __repr__(self):
        out = [
            f"added_authenticated_peers={self.added_authenticated_peers}",
            f"dropped_authenticated_peers={self.dropped_authenticated_peers}",
            f"total_inbound_peer_count={self.total_inbound_peer_count}",
            f"total_outbound_peer_count={self.total_outbound_peer_count}",
            f"p75_scp_first_to_self_latency_ms={self.p75_scp_first_to_self_latency_ms}",
            f"p75_scp_self_to_other_latency_ms={self.p75_scp_self_to_other_latency_ms}",
            f"lost_sync_count={self.lost_sync_count}",
            f"is_validator={self.is_validator}",
            f"max_inbound_peer_count={self.max_inbound_peer_count}",
            f"max_outbound_peer_count={self.max_outbound_peer_count}",
        ]
        return f"<TimeSlicedNodeData [{', '.join(out)}]>"
