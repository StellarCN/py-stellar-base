# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .hash import Hash
from .scp_ballot import SCPBallot
from .uint32 import Uint32

__all__ = ["SCPStatementConfirm"]


class SCPStatementConfirm:
    """
    XDR Source Code::

        struct
                {
                    SCPBallot ballot;   // b
                    uint32 nPrepared;   // p.n
                    uint32 nCommit;     // c.n
                    uint32 nH;          // h.n
                    Hash quorumSetHash; // D
                }
    """

    def __init__(
        self,
        ballot: SCPBallot,
        n_prepared: Uint32,
        n_commit: Uint32,
        n_h: Uint32,
        quorum_set_hash: Hash,
    ) -> None:
        self.ballot = ballot
        self.n_prepared = n_prepared
        self.n_commit = n_commit
        self.n_h = n_h
        self.quorum_set_hash = quorum_set_hash

    def pack(self, packer: Packer) -> None:
        self.ballot.pack(packer)
        self.n_prepared.pack(packer)
        self.n_commit.pack(packer)
        self.n_h.pack(packer)
        self.quorum_set_hash.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCPStatementConfirm:
        ballot = SCPBallot.unpack(unpacker)
        n_prepared = Uint32.unpack(unpacker)
        n_commit = Uint32.unpack(unpacker)
        n_h = Uint32.unpack(unpacker)
        quorum_set_hash = Hash.unpack(unpacker)
        return cls(
            ballot=ballot,
            n_prepared=n_prepared,
            n_commit=n_commit,
            n_h=n_h,
            quorum_set_hash=quorum_set_hash,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCPStatementConfirm:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCPStatementConfirm:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.ballot,
                self.n_prepared,
                self.n_commit,
                self.n_h,
                self.quorum_set_hash,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ballot == other.ballot
            and self.n_prepared == other.n_prepared
            and self.n_commit == other.n_commit
            and self.n_h == other.n_h
            and self.quorum_set_hash == other.quorum_set_hash
        )

    def __repr__(self):
        out = [
            f"ballot={self.ballot}",
            f"n_prepared={self.n_prepared}",
            f"n_commit={self.n_commit}",
            f"n_h={self.n_h}",
            f"quorum_set_hash={self.quorum_set_hash}",
        ]
        return f"<SCPStatementConfirm [{', '.join(out)}]>"
