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

__all__ = ["SCPStatementExternalize"]


class SCPStatementExternalize:
    """
    XDR Source Code::

        struct
                {
                    SCPBallot commit;         // c
                    uint32 nH;                // h.n
                    Hash commitQuorumSetHash; // D used before EXTERNALIZE
                }
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCPStatementExternalize:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        commit = SCPBallot.unpack(unpacker, depth_limit - 1)
        n_h = Uint32.unpack(unpacker, depth_limit - 1)
        commit_quorum_set_hash = Hash.unpack(unpacker, depth_limit - 1)
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
    def from_xdr_bytes(cls, xdr: bytes) -> SCPStatementExternalize:
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
    def from_xdr(cls, xdr: str) -> SCPStatementExternalize:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCPStatementExternalize:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "commit": self.commit.to_json_dict(),
            "n_h": self.n_h.to_json_dict(),
            "commit_quorum_set_hash": self.commit_quorum_set_hash.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SCPStatementExternalize:
        commit = SCPBallot.from_json_dict(json_dict["commit"])
        n_h = Uint32.from_json_dict(json_dict["n_h"])
        commit_quorum_set_hash = Hash.from_json_dict(
            json_dict["commit_quorum_set_hash"]
        )
        return cls(
            commit=commit,
            n_h=n_h,
            commit_quorum_set_hash=commit_quorum_set_hash,
        )

    def __hash__(self):
        return hash(
            (
                self.commit,
                self.n_h,
                self.commit_quorum_set_hash,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.commit == other.commit
            and self.n_h == other.n_h
            and self.commit_quorum_set_hash == other.commit_quorum_set_hash
        )

    def __repr__(self):
        out = [
            f"commit={self.commit}",
            f"n_h={self.n_h}",
            f"commit_quorum_set_hash={self.commit_quorum_set_hash}",
        ]
        return f"<SCPStatementExternalize [{', '.join(out)}]>"
