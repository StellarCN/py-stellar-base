# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import Optional
from xdrlib import Packer, Unpacker

from .hash import Hash
from .scp_ballot import SCPBallot
from .uint32 import Uint32

__all__ = ["SCPStatementPrepare"]


class SCPStatementPrepare:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct
            {
                Hash quorumSetHash;       // D
                SCPBallot ballot;         // b
                SCPBallot* prepared;      // p
                SCPBallot* preparedPrime; // p'
                uint32 nC;                // c.n
                uint32 nH;                // h.n
            }
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        quorum_set_hash: Hash,
        ballot: SCPBallot,
        prepared: Optional[SCPBallot],
        prepared_prime: Optional[SCPBallot],
        n_c: Uint32,
        n_h: Uint32,
    ) -> None:
        self.quorum_set_hash = quorum_set_hash
        self.ballot = ballot
        self.prepared = prepared
        self.prepared_prime = prepared_prime
        self.n_c = n_c
        self.n_h = n_h

    def pack(self, packer: Packer) -> None:
        self.quorum_set_hash.pack(packer)
        self.ballot.pack(packer)
        if self.prepared is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.prepared.pack(packer)
        if self.prepared_prime is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.prepared_prime.pack(packer)
        self.n_c.pack(packer)
        self.n_h.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCPStatementPrepare":
        quorum_set_hash = Hash.unpack(unpacker)
        ballot = SCPBallot.unpack(unpacker)
        prepared = SCPBallot.unpack(unpacker) if unpacker.unpack_uint() else None
        prepared_prime = SCPBallot.unpack(unpacker) if unpacker.unpack_uint() else None
        n_c = Uint32.unpack(unpacker)
        n_h = Uint32.unpack(unpacker)
        return cls(
            quorum_set_hash=quorum_set_hash,
            ballot=ballot,
            prepared=prepared,
            prepared_prime=prepared_prime,
            n_c=n_c,
            n_h=n_h,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCPStatementPrepare":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCPStatementPrepare":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.quorum_set_hash == other.quorum_set_hash
            and self.ballot == other.ballot
            and self.prepared == other.prepared
            and self.prepared_prime == other.prepared_prime
            and self.n_c == other.n_c
            and self.n_h == other.n_h
        )

    def __str__(self):
        out = [
            f"quorum_set_hash={self.quorum_set_hash}",
            f"ballot={self.ballot}",
            f"prepared={self.prepared}",
            f"prepared_prime={self.prepared_prime}",
            f"n_c={self.n_c}",
            f"n_h={self.n_h}",
        ]
        return f"<SCPStatementPrepare {[', '.join(out)]}>"
