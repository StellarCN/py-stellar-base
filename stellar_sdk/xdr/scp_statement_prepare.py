# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .hash import Hash
from .scp_ballot import SCPBallot
from .uint32 import Uint32

__all__ = ["SCPStatementPrepare"]


class SCPStatementPrepare:
    """
    XDR Source Code::

        struct
                {
                    Hash quorumSetHash;       // D
                    SCPBallot ballot;         // b
                    SCPBallot* prepared;      // p
                    SCPBallot* preparedPrime; // p'
                    uint32 nC;                // c.n
                    uint32 nH;                // h.n
                }
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCPStatementPrepare:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        quorum_set_hash = Hash.unpack(unpacker, depth_limit - 1)
        ballot = SCPBallot.unpack(unpacker, depth_limit - 1)
        prepared = (
            SCPBallot.unpack(unpacker, depth_limit - 1)
            if unpacker.unpack_uint()
            else None
        )
        prepared_prime = (
            SCPBallot.unpack(unpacker, depth_limit - 1)
            if unpacker.unpack_uint()
            else None
        )
        n_c = Uint32.unpack(unpacker, depth_limit - 1)
        n_h = Uint32.unpack(unpacker, depth_limit - 1)
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
    def from_xdr_bytes(cls, xdr: bytes) -> SCPStatementPrepare:
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
    def from_xdr(cls, xdr: str) -> SCPStatementPrepare:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCPStatementPrepare:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "quorum_set_hash": self.quorum_set_hash.to_json_dict(),
            "ballot": self.ballot.to_json_dict(),
            "prepared": (
                self.prepared.to_json_dict() if self.prepared is not None else None
            ),
            "prepared_prime": (
                self.prepared_prime.to_json_dict()
                if self.prepared_prime is not None
                else None
            ),
            "n_c": self.n_c.to_json_dict(),
            "n_h": self.n_h.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SCPStatementPrepare:
        quorum_set_hash = Hash.from_json_dict(json_dict["quorum_set_hash"])
        ballot = SCPBallot.from_json_dict(json_dict["ballot"])
        prepared = (
            SCPBallot.from_json_dict(json_dict["prepared"])
            if json_dict["prepared"] is not None
            else None
        )
        prepared_prime = (
            SCPBallot.from_json_dict(json_dict["prepared_prime"])
            if json_dict["prepared_prime"] is not None
            else None
        )
        n_c = Uint32.from_json_dict(json_dict["n_c"])
        n_h = Uint32.from_json_dict(json_dict["n_h"])
        return cls(
            quorum_set_hash=quorum_set_hash,
            ballot=ballot,
            prepared=prepared,
            prepared_prime=prepared_prime,
            n_c=n_c,
            n_h=n_h,
        )

    def __hash__(self):
        return hash(
            (
                self.quorum_set_hash,
                self.ballot,
                self.prepared,
                self.prepared_prime,
                self.n_c,
                self.n_h,
            )
        )

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

    def __repr__(self):
        out = [
            f"quorum_set_hash={self.quorum_set_hash}",
            f"ballot={self.ballot}",
            f"prepared={self.prepared}",
            f"prepared_prime={self.prepared_prime}",
            f"n_c={self.n_c}",
            f"n_h={self.n_h}",
        ]
        return f"<SCPStatementPrepare [{', '.join(out)}]>"
