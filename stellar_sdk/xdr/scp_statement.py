# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .node_id import NodeID
from .scp_statement_pledges import SCPStatementPledges
from .uint64 import Uint64

__all__ = ["SCPStatement"]


class SCPStatement:
    """
    XDR Source Code::

        struct SCPStatement
        {
            NodeID nodeID;    // v
            uint64 slotIndex; // i

            union switch (SCPStatementType type)
            {
            case SCP_ST_PREPARE:
                struct
                {
                    Hash quorumSetHash;       // D
                    SCPBallot ballot;         // b
                    SCPBallot* prepared;      // p
                    SCPBallot* preparedPrime; // p'
                    uint32 nC;                // c.n
                    uint32 nH;                // h.n
                } prepare;
            case SCP_ST_CONFIRM:
                struct
                {
                    SCPBallot ballot;   // b
                    uint32 nPrepared;   // p.n
                    uint32 nCommit;     // c.n
                    uint32 nH;          // h.n
                    Hash quorumSetHash; // D
                } confirm;
            case SCP_ST_EXTERNALIZE:
                struct
                {
                    SCPBallot commit;         // c
                    uint32 nH;                // h.n
                    Hash commitQuorumSetHash; // D used before EXTERNALIZE
                } externalize;
            case SCP_ST_NOMINATE:
                SCPNomination nominate;
            }
            pledges;
        };
    """

    def __init__(
        self,
        node_id: NodeID,
        slot_index: Uint64,
        pledges: SCPStatementPledges,
    ) -> None:
        self.node_id = node_id
        self.slot_index = slot_index
        self.pledges = pledges

    def pack(self, packer: Packer) -> None:
        self.node_id.pack(packer)
        self.slot_index.pack(packer)
        self.pledges.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCPStatement:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        node_id = NodeID.unpack(unpacker, depth_limit - 1)
        slot_index = Uint64.unpack(unpacker, depth_limit - 1)
        pledges = SCPStatementPledges.unpack(unpacker, depth_limit - 1)
        return cls(
            node_id=node_id,
            slot_index=slot_index,
            pledges=pledges,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCPStatement:
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
    def from_xdr(cls, xdr: str) -> SCPStatement:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCPStatement:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "node_id": self.node_id.to_json_dict(),
            "slot_index": self.slot_index.to_json_dict(),
            "pledges": self.pledges.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SCPStatement:
        node_id = NodeID.from_json_dict(json_dict["node_id"])
        slot_index = Uint64.from_json_dict(json_dict["slot_index"])
        pledges = SCPStatementPledges.from_json_dict(json_dict["pledges"])
        return cls(
            node_id=node_id,
            slot_index=slot_index,
            pledges=pledges,
        )

    def __hash__(self):
        return hash(
            (
                self.node_id,
                self.slot_index,
                self.pledges,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.node_id == other.node_id
            and self.slot_index == other.slot_index
            and self.pledges == other.pledges
        )

    def __repr__(self):
        out = [
            f"node_id={self.node_id}",
            f"slot_index={self.slot_index}",
            f"pledges={self.pledges}",
        ]
        return f"<SCPStatement [{', '.join(out)}]>"
