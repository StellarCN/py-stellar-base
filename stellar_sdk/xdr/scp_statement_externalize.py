# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .hash import Hash
from .scp_ballot import SCPBallot
from .uint32 import Uint32

__all__ = ["SCPStatementExternalize"]


class SCPStatementExternalize:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct
            {
                SCPBallot commit;         // c
                uint32 nH;                // h.n
                Hash commitQuorumSetHash; // D used before EXTERNALIZE
            }
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        commit: SCPBallot,
        n_h: Uint32,
        commit_quorum_set_hash: Hash,
    ) -> None:
        self.commit = commit
        self.n_h = n_h
        self.commit_quorum_set_hash = commit_quorum_set_hash

    def pack(self, packer: Packer) -> None:
        self.commit.pack(packer)
        self.n_h.pack(packer)
        self.commit_quorum_set_hash.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCPStatementExternalize":
        commit = SCPBallot.unpack(unpacker)
        n_h = Uint32.unpack(unpacker)
        commit_quorum_set_hash = Hash.unpack(unpacker)
        return cls(
            commit=commit,
            n_h=n_h,
            commit_quorum_set_hash=commit_quorum_set_hash,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCPStatementExternalize":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCPStatementExternalize":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.commit == other.commit
            and self.n_h == other.n_h
            and self.commit_quorum_set_hash == other.commit_quorum_set_hash
        )

    def __str__(self):
        out = [
            f"commit={self.commit}",
            f"n_h={self.n_h}",
            f"commit_quorum_set_hash={self.commit_quorum_set_hash}",
        ]
        return f"<SCPStatementExternalize {[', '.join(out)]}>"
