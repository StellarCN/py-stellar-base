# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib import Packer, Unpacker

from .ledger_scp_messages import LedgerSCPMessages
from .scp_quorum_set import SCPQuorumSet
from ..exceptions import ValueError

__all__ = ["SCPHistoryEntryV0"]


class SCPHistoryEntryV0:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct SCPHistoryEntryV0
    {
        SCPQuorumSet quorumSets<>; // additional quorum sets used by ledgerMessages
        LedgerSCPMessages ledgerMessages;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        quorum_sets: List[SCPQuorumSet],
        ledger_messages: LedgerSCPMessages,
    ) -> None:
        if quorum_sets and len(quorum_sets) > 4294967295:
            raise ValueError(
                f"The maximum length of `quorum_sets` should be 4294967295, but got {len(quorum_sets)}."
            )
        self.quorum_sets = quorum_sets
        self.ledger_messages = ledger_messages

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.quorum_sets))
        for quorum_set in self.quorum_sets:
            quorum_set.pack(packer)
        self.ledger_messages.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCPHistoryEntryV0":
        length = unpacker.unpack_uint()
        quorum_sets = []
        for _ in range(length):
            quorum_sets.append(SCPQuorumSet.unpack(unpacker))
        ledger_messages = LedgerSCPMessages.unpack(unpacker)
        return cls(
            quorum_sets=quorum_sets,
            ledger_messages=ledger_messages,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCPHistoryEntryV0":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCPHistoryEntryV0":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.quorum_sets == other.quorum_sets
            and self.ledger_messages == other.ledger_messages
        )

    def __str__(self):
        out = [
            f"quorum_sets={self.quorum_sets}",
            f"ledger_messages={self.ledger_messages}",
        ]
        return f"<SCPHistoryEntryV0 {[', '.join(out)]}>"
