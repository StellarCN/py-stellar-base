# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

from .cold_archive_bucket_entry import ColdArchiveBucketEntry
from .proof_level import ProofLevel

__all__ = ["NonexistenceProofBody"]


class NonexistenceProofBody:
    """
    XDR Source Code::

        struct NonexistenceProofBody
        {
            ColdArchiveBucketEntry entriesToProve<>;

            // Vector of vectors, where proofLevels[level]
            // contains all HashNodes that correspond with that level
            ProofLevel proofLevels<>;
        };
    """

    def __init__(
        self,
        entries_to_prove: List[ColdArchiveBucketEntry],
        proof_levels: List[ProofLevel],
    ) -> None:
        _expect_max_length = 4294967295
        if entries_to_prove and len(entries_to_prove) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `entries_to_prove` should be {_expect_max_length}, but got {len(entries_to_prove)}."
            )
        _expect_max_length = 4294967295
        if proof_levels and len(proof_levels) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `proof_levels` should be {_expect_max_length}, but got {len(proof_levels)}."
            )
        self.entries_to_prove = entries_to_prove
        self.proof_levels = proof_levels

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.entries_to_prove))
        for entries_to_prove_item in self.entries_to_prove:
            entries_to_prove_item.pack(packer)
        packer.pack_uint(len(self.proof_levels))
        for proof_levels_item in self.proof_levels:
            proof_levels_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> NonexistenceProofBody:
        length = unpacker.unpack_uint()
        entries_to_prove = []
        for _ in range(length):
            entries_to_prove.append(ColdArchiveBucketEntry.unpack(unpacker))
        length = unpacker.unpack_uint()
        proof_levels = []
        for _ in range(length):
            proof_levels.append(ProofLevel.unpack(unpacker))
        return cls(
            entries_to_prove=entries_to_prove,
            proof_levels=proof_levels,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> NonexistenceProofBody:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> NonexistenceProofBody:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.entries_to_prove,
                self.proof_levels,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.entries_to_prove == other.entries_to_prove
            and self.proof_levels == other.proof_levels
        )

    def __repr__(self):
        out = [
            f"entries_to_prove={self.entries_to_prove}",
            f"proof_levels={self.proof_levels}",
        ]
        return f"<NonexistenceProofBody [{', '.join(out)}]>"
