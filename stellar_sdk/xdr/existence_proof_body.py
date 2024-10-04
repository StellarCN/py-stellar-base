# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

from .cold_archive_bucket_entry import ColdArchiveBucketEntry
from .ledger_key import LedgerKey
from .proof_level import ProofLevel

__all__ = ["ExistenceProofBody"]


class ExistenceProofBody:
    """
    XDR Source Code::

        struct ExistenceProofBody
        {
            LedgerKey keysToProve<>;

            // Bounds for each key being proved, where bound[n]
            // corresponds to keysToProve[n]
            ColdArchiveBucketEntry lowBoundEntries<>;
            ColdArchiveBucketEntry highBoundEntries<>;

            // Vector of vectors, where proofLevels[level]
            // contains all HashNodes that correspond with that level
            ProofLevel proofLevels<>;
        };
    """

    def __init__(
        self,
        keys_to_prove: List[LedgerKey],
        low_bound_entries: List[ColdArchiveBucketEntry],
        high_bound_entries: List[ColdArchiveBucketEntry],
        proof_levels: List[ProofLevel],
    ) -> None:
        _expect_max_length = 4294967295
        if keys_to_prove and len(keys_to_prove) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `keys_to_prove` should be {_expect_max_length}, but got {len(keys_to_prove)}."
            )
        _expect_max_length = 4294967295
        if low_bound_entries and len(low_bound_entries) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `low_bound_entries` should be {_expect_max_length}, but got {len(low_bound_entries)}."
            )
        _expect_max_length = 4294967295
        if high_bound_entries and len(high_bound_entries) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `high_bound_entries` should be {_expect_max_length}, but got {len(high_bound_entries)}."
            )
        _expect_max_length = 4294967295
        if proof_levels and len(proof_levels) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `proof_levels` should be {_expect_max_length}, but got {len(proof_levels)}."
            )
        self.keys_to_prove = keys_to_prove
        self.low_bound_entries = low_bound_entries
        self.high_bound_entries = high_bound_entries
        self.proof_levels = proof_levels

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.keys_to_prove))
        for keys_to_prove_item in self.keys_to_prove:
            keys_to_prove_item.pack(packer)
        packer.pack_uint(len(self.low_bound_entries))
        for low_bound_entries_item in self.low_bound_entries:
            low_bound_entries_item.pack(packer)
        packer.pack_uint(len(self.high_bound_entries))
        for high_bound_entries_item in self.high_bound_entries:
            high_bound_entries_item.pack(packer)
        packer.pack_uint(len(self.proof_levels))
        for proof_levels_item in self.proof_levels:
            proof_levels_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ExistenceProofBody:
        length = unpacker.unpack_uint()
        keys_to_prove = []
        for _ in range(length):
            keys_to_prove.append(LedgerKey.unpack(unpacker))
        length = unpacker.unpack_uint()
        low_bound_entries = []
        for _ in range(length):
            low_bound_entries.append(ColdArchiveBucketEntry.unpack(unpacker))
        length = unpacker.unpack_uint()
        high_bound_entries = []
        for _ in range(length):
            high_bound_entries.append(ColdArchiveBucketEntry.unpack(unpacker))
        length = unpacker.unpack_uint()
        proof_levels = []
        for _ in range(length):
            proof_levels.append(ProofLevel.unpack(unpacker))
        return cls(
            keys_to_prove=keys_to_prove,
            low_bound_entries=low_bound_entries,
            high_bound_entries=high_bound_entries,
            proof_levels=proof_levels,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ExistenceProofBody:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ExistenceProofBody:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.keys_to_prove,
                self.low_bound_entries,
                self.high_bound_entries,
                self.proof_levels,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.keys_to_prove == other.keys_to_prove
            and self.low_bound_entries == other.low_bound_entries
            and self.high_bound_entries == other.high_bound_entries
            and self.proof_levels == other.proof_levels
        )

    def __repr__(self):
        out = [
            f"keys_to_prove={self.keys_to_prove}",
            f"low_bound_entries={self.low_bound_entries}",
            f"high_bound_entries={self.high_bound_entries}",
            f"proof_levels={self.proof_levels}",
        ]
        return f"<ExistenceProofBody [{', '.join(out)}]>"
