# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .archival_proof_body import ArchivalProofBody
from .uint32 import Uint32

__all__ = ["ArchivalProof"]


class ArchivalProof:
    """
    XDR Source Code::

        struct ArchivalProof
        {
            uint32 epoch; // AST Subtree for this proof

            union switch (ArchivalProofType t)
            {
            case EXISTENCE:
                NonexistenceProofBody nonexistenceProof;
            case NONEXISTENCE:
                ExistenceProofBody existenceProof;
            } body;
        };
    """

    def __init__(
        self,
        epoch: Uint32,
        body: ArchivalProofBody,
    ) -> None:
        self.epoch = epoch
        self.body = body

    def pack(self, packer: Packer) -> None:
        self.epoch.pack(packer)
        self.body.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ArchivalProof:
        epoch = Uint32.unpack(unpacker)
        body = ArchivalProofBody.unpack(unpacker)
        return cls(
            epoch=epoch,
            body=body,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ArchivalProof:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ArchivalProof:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.epoch,
                self.body,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.epoch == other.epoch and self.body == other.body

    def __repr__(self):
        out = [
            f"epoch={self.epoch}",
            f"body={self.body}",
        ]
        return f"<ArchivalProof [{', '.join(out)}]>"
