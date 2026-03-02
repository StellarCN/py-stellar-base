# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCPStatementConfirm:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        ballot = SCPBallot.unpack(unpacker, depth_limit - 1)
        n_prepared = Uint32.unpack(unpacker, depth_limit - 1)
        n_commit = Uint32.unpack(unpacker, depth_limit - 1)
        n_h = Uint32.unpack(unpacker, depth_limit - 1)
        quorum_set_hash = Hash.unpack(unpacker, depth_limit - 1)
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCPStatementConfirm:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCPStatementConfirm:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "ballot": self.ballot.to_json_dict(),
            "n_prepared": self.n_prepared.to_json_dict(),
            "n_commit": self.n_commit.to_json_dict(),
            "n_h": self.n_h.to_json_dict(),
            "quorum_set_hash": self.quorum_set_hash.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SCPStatementConfirm:
        ballot = SCPBallot.from_json_dict(json_dict["ballot"])
        n_prepared = Uint32.from_json_dict(json_dict["n_prepared"])
        n_commit = Uint32.from_json_dict(json_dict["n_commit"])
        n_h = Uint32.from_json_dict(json_dict["n_h"])
        quorum_set_hash = Hash.from_json_dict(json_dict["quorum_set_hash"])
        return cls(
            ballot=ballot,
            n_prepared=n_prepared,
            n_commit=n_commit,
            n_h=n_h,
            quorum_set_hash=quorum_set_hash,
        )

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
