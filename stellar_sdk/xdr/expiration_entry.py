# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .hash import Hash
from .uint32 import Uint32

__all__ = ["ExpirationEntry"]


class ExpirationEntry:
    """
    XDR Source Code::

        struct ExpirationEntry {
            // Hash of the LedgerKey that is associated with this ExpirationEntry
            Hash keyHash;
            uint32 expirationLedgerSeq;
        };
    """

    def __init__(
        self,
        key_hash: Hash,
        expiration_ledger_seq: Uint32,
    ) -> None:
        self.key_hash = key_hash
        self.expiration_ledger_seq = expiration_ledger_seq

    def pack(self, packer: Packer) -> None:
        self.key_hash.pack(packer)
        self.expiration_ledger_seq.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ExpirationEntry:
        key_hash = Hash.unpack(unpacker)
        expiration_ledger_seq = Uint32.unpack(unpacker)
        return cls(
            key_hash=key_hash,
            expiration_ledger_seq=expiration_ledger_seq,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ExpirationEntry:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ExpirationEntry:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.key_hash,
                self.expiration_ledger_seq,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.key_hash == other.key_hash
            and self.expiration_ledger_seq == other.expiration_ledger_seq
        )

    def __str__(self):
        out = [
            f"key_hash={self.key_hash}",
            f"expiration_ledger_seq={self.expiration_ledger_seq}",
        ]
        return f"<ExpirationEntry [{', '.join(out)}]>"
