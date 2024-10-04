# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .archival_proof_type import ArchivalProofType
from .existence_proof_body import ExistenceProofBody
from .nonexistence_proof_body import NonexistenceProofBody

__all__ = ["ArchivalProofBody"]


class ArchivalProofBody:
    """
    XDR Source Code::

        union switch (ArchivalProofType t)
            {
            case EXISTENCE:
                NonexistenceProofBody nonexistenceProof;
            case NONEXISTENCE:
                ExistenceProofBody existenceProof;
            }
    """

    def __init__(
        self,
        t: ArchivalProofType,
        nonexistence_proof: NonexistenceProofBody = None,
        existence_proof: ExistenceProofBody = None,
    ) -> None:
        self.t = t
        self.nonexistence_proof = nonexistence_proof
        self.existence_proof = existence_proof

    def pack(self, packer: Packer) -> None:
        self.t.pack(packer)
        if self.t == ArchivalProofType.EXISTENCE:
            if self.nonexistence_proof is None:
                raise ValueError("nonexistence_proof should not be None.")
            self.nonexistence_proof.pack(packer)
            return
        if self.t == ArchivalProofType.NONEXISTENCE:
            if self.existence_proof is None:
                raise ValueError("existence_proof should not be None.")
            self.existence_proof.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ArchivalProofBody:
        t = ArchivalProofType.unpack(unpacker)
        if t == ArchivalProofType.EXISTENCE:
            nonexistence_proof = NonexistenceProofBody.unpack(unpacker)
            return cls(t=t, nonexistence_proof=nonexistence_proof)
        if t == ArchivalProofType.NONEXISTENCE:
            existence_proof = ExistenceProofBody.unpack(unpacker)
            return cls(t=t, existence_proof=existence_proof)
        return cls(t=t)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ArchivalProofBody:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ArchivalProofBody:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.t,
                self.nonexistence_proof,
                self.existence_proof,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.t == other.t
            and self.nonexistence_proof == other.nonexistence_proof
            and self.existence_proof == other.existence_proof
        )

    def __repr__(self):
        out = []
        out.append(f"t={self.t}")
        (
            out.append(f"nonexistence_proof={self.nonexistence_proof}")
            if self.nonexistence_proof is not None
            else None
        )
        (
            out.append(f"existence_proof={self.existence_proof}")
            if self.existence_proof is not None
            else None
        )
        return f"<ArchivalProofBody [{', '.join(out)}]>"
