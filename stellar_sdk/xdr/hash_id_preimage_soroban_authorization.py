# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .hash import Hash
from .int64 import Int64
from .soroban_authorized_invocation import SorobanAuthorizedInvocation
from .uint32 import Uint32

__all__ = ["HashIDPreimageSorobanAuthorization"]


class HashIDPreimageSorobanAuthorization:
    """
    XDR Source Code::

        struct
            {
                Hash networkID;
                int64 nonce;
                uint32 signatureExpirationLedger;
                SorobanAuthorizedInvocation invocation;
            }
    """

    def __init__(
        self,
        network_id: Hash,
        nonce: Int64,
        signature_expiration_ledger: Uint32,
        invocation: SorobanAuthorizedInvocation,
    ) -> None:
        self.network_id = network_id
        self.nonce = nonce
        self.signature_expiration_ledger = signature_expiration_ledger
        self.invocation = invocation

    def pack(self, packer: Packer) -> None:
        self.network_id.pack(packer)
        self.nonce.pack(packer)
        self.signature_expiration_ledger.pack(packer)
        self.invocation.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> HashIDPreimageSorobanAuthorization:
        network_id = Hash.unpack(unpacker)
        nonce = Int64.unpack(unpacker)
        signature_expiration_ledger = Uint32.unpack(unpacker)
        invocation = SorobanAuthorizedInvocation.unpack(unpacker)
        return cls(
            network_id=network_id,
            nonce=nonce,
            signature_expiration_ledger=signature_expiration_ledger,
            invocation=invocation,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> HashIDPreimageSorobanAuthorization:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> HashIDPreimageSorobanAuthorization:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.network_id,
                self.nonce,
                self.signature_expiration_ledger,
                self.invocation,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.network_id == other.network_id
            and self.nonce == other.nonce
            and self.signature_expiration_ledger == other.signature_expiration_ledger
            and self.invocation == other.invocation
        )

    def __repr__(self):
        out = [
            f"network_id={self.network_id}",
            f"nonce={self.nonce}",
            f"signature_expiration_ledger={self.signature_expiration_ledger}",
            f"invocation={self.invocation}",
        ]
        return f"<HashIDPreimageSorobanAuthorization [{', '.join(out)}]>"
