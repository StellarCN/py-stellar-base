# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

from .archival_proof_node import ArchivalProofNode

__all__ = ["ProofLevel"]


class ProofLevel:
    """
    XDR Source Code::

        typedef ArchivalProofNode ProofLevel<>;
    """

    def __init__(self, proof_level: List[ArchivalProofNode]) -> None:
        _expect_max_length = 4294967295
        if proof_level and len(proof_level) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `proof_level` should be {_expect_max_length}, but got {len(proof_level)}."
            )
        self.proof_level = proof_level

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.proof_level))
        for proof_level_item in self.proof_level:
            proof_level_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ProofLevel:
        length = unpacker.unpack_uint()
        proof_level = []
        for _ in range(length):
            proof_level.append(ArchivalProofNode.unpack(unpacker))
        return cls(proof_level)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ProofLevel:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ProofLevel:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(self.proof_level)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.proof_level == other.proof_level

    def __repr__(self):
        return f"<ProofLevel [proof_level={self.proof_level}]>"
