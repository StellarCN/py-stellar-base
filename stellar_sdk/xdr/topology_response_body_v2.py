# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .time_sliced_node_data import TimeSlicedNodeData
from .time_sliced_peer_data_list import TimeSlicedPeerDataList

__all__ = ["TopologyResponseBodyV2"]


class TopologyResponseBodyV2:
    """
    XDR Source Code::

        struct TopologyResponseBodyV2
        {
            TimeSlicedPeerDataList inboundPeers;
            TimeSlicedPeerDataList outboundPeers;
            TimeSlicedNodeData nodeData;
        };
    """

    def __init__(
        self,
        inbound_peers: TimeSlicedPeerDataList,
        outbound_peers: TimeSlicedPeerDataList,
        node_data: TimeSlicedNodeData,
    ) -> None:
        self.inbound_peers = inbound_peers
        self.outbound_peers = outbound_peers
        self.node_data = node_data

    def pack(self, packer: Packer) -> None:
        self.inbound_peers.pack(packer)
        self.outbound_peers.pack(packer)
        self.node_data.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> TopologyResponseBodyV2:
        inbound_peers = TimeSlicedPeerDataList.unpack(unpacker)
        outbound_peers = TimeSlicedPeerDataList.unpack(unpacker)
        node_data = TimeSlicedNodeData.unpack(unpacker)
        return cls(
            inbound_peers=inbound_peers,
            outbound_peers=outbound_peers,
            node_data=node_data,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TopologyResponseBodyV2:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> TopologyResponseBodyV2:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.inbound_peers,
                self.outbound_peers,
                self.node_data,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.inbound_peers == other.inbound_peers
            and self.outbound_peers == other.outbound_peers
            and self.node_data == other.node_data
        )

    def __repr__(self):
        out = [
            f"inbound_peers={self.inbound_peers}",
            f"outbound_peers={self.outbound_peers}",
            f"node_data={self.node_data}",
        ]
        return f"<TopologyResponseBodyV2 [{', '.join(out)}]>"
