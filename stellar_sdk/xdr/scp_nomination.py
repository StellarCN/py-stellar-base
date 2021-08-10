# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib import Packer, Unpacker

from ..exceptions import ValueError
from .hash import Hash
from .value import Value

__all__ = ["SCPNomination"]


class SCPNomination:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct SCPNomination
    {
        Hash quorumSetHash; // D
        Value votes<>;      // X
        Value accepted<>;   // Y
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        quorum_set_hash: Hash,
        votes: List[Value],
        accepted: List[Value],
    ) -> None:
        if votes and len(votes) > 4294967295:
            raise ValueError(
                f"The maximum length of `votes` should be 4294967295, but got {len(votes)}."
            )
        if accepted and len(accepted) > 4294967295:
            raise ValueError(
                f"The maximum length of `accepted` should be 4294967295, but got {len(accepted)}."
            )
        self.quorum_set_hash = quorum_set_hash
        self.votes = votes
        self.accepted = accepted

    def pack(self, packer: Packer) -> None:
        self.quorum_set_hash.pack(packer)
        packer.pack_uint(len(self.votes))
        for vote in self.votes:
            vote.pack(packer)
        packer.pack_uint(len(self.accepted))
        for accepted in self.accepted:
            accepted.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCPNomination":
        quorum_set_hash = Hash.unpack(unpacker)
        length = unpacker.unpack_uint()
        votes = []
        for _ in range(length):
            votes.append(Value.unpack(unpacker))
        length = unpacker.unpack_uint()
        accepted = []
        for _ in range(length):
            accepted.append(Value.unpack(unpacker))
        return cls(
            quorum_set_hash=quorum_set_hash,
            votes=votes,
            accepted=accepted,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCPNomination":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCPNomination":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.quorum_set_hash == other.quorum_set_hash
            and self.votes == other.votes
            and self.accepted == other.accepted
        )

    def __str__(self):
        out = [
            f"quorum_set_hash={self.quorum_set_hash}",
            f"votes={self.votes}",
            f"accepted={self.accepted}",
        ]
        return f"<SCPNomination {[', '.join(out)]}>"
