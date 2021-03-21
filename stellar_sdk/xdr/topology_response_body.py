# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .peer_stat_list import PeerStatList
from .uint32 import Uint32

__all__ = ["TopologyResponseBody"]


class TopologyResponseBody:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct TopologyResponseBody
    {
        PeerStatList inboundPeers;
        PeerStatList outboundPeers;

        uint32 totalInboundPeerCount;
        uint32 totalOutboundPeerCount;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        inbound_peers: PeerStatList,
        outbound_peers: PeerStatList,
        total_inbound_peer_count: Uint32,
        total_outbound_peer_count: Uint32,
    ) -> None:
        self.inbound_peers = inbound_peers
        self.outbound_peers = outbound_peers
        self.total_inbound_peer_count = total_inbound_peer_count
        self.total_outbound_peer_count = total_outbound_peer_count

    def pack(self, packer: Packer) -> None:
        self.inbound_peers.pack(packer)
        self.outbound_peers.pack(packer)
        self.total_inbound_peer_count.pack(packer)
        self.total_outbound_peer_count.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TopologyResponseBody":
        inbound_peers = PeerStatList.unpack(unpacker)
        outbound_peers = PeerStatList.unpack(unpacker)
        total_inbound_peer_count = Uint32.unpack(unpacker)
        total_outbound_peer_count = Uint32.unpack(unpacker)
        return cls(
            inbound_peers=inbound_peers,
            outbound_peers=outbound_peers,
            total_inbound_peer_count=total_inbound_peer_count,
            total_outbound_peer_count=total_outbound_peer_count,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "TopologyResponseBody":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TopologyResponseBody":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.inbound_peers == other.inbound_peers
            and self.outbound_peers == other.outbound_peers
            and self.total_inbound_peer_count == other.total_inbound_peer_count
            and self.total_outbound_peer_count == other.total_outbound_peer_count
        )

    def __str__(self):
        out = [
            f"inbound_peers={self.inbound_peers}",
            f"outbound_peers={self.outbound_peers}",
            f"total_inbound_peer_count={self.total_inbound_peer_count}",
            f"total_outbound_peer_count={self.total_outbound_peer_count}",
        ]
        return f"<TopologyResponseBody {[', '.join(out)]}>"
