# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .node_id import NodeID
from .scp_statement_pledges import SCPStatementPledges
from .uint64 import Uint64

__all__ = ["SCPStatement"]


class SCPStatement:
    """
    XDR Source Code
    ----------------------------------------------------------------
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
    ----------------------------------------------------------------
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
    def unpack(cls, unpacker: Unpacker) -> "SCPStatement":
        node_id = NodeID.unpack(unpacker)
        slot_index = Uint64.unpack(unpacker)
        pledges = SCPStatementPledges.unpack(unpacker)
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
    def from_xdr_bytes(cls, xdr: bytes) -> "SCPStatement":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCPStatement":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.node_id == other.node_id
            and self.slot_index == other.slot_index
            and self.pledges == other.pledges
        )

    def __str__(self):
        out = [
            f"node_id={self.node_id}",
            f"slot_index={self.slot_index}",
            f"pledges={self.pledges}",
        ]
        return f"<SCPStatement {[', '.join(out)]}>"
