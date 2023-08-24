# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .contract_code_entry_body import ContractCodeEntryBody
from .extension_point import ExtensionPoint
from .hash import Hash
from .uint32 import Uint32

__all__ = ["ContractCodeEntry"]


class ContractCodeEntry:
    """
    XDR Source Code::

        struct ContractCodeEntry {
            ExtensionPoint ext;

            Hash hash;
            union switch (ContractEntryBodyType bodyType)
            {
            case DATA_ENTRY:
                opaque code<>;
            case EXPIRATION_EXTENSION:
                void;
            } body;

            uint32 expirationLedgerSeq;
        };
    """

    def __init__(
        self,
        ext: ExtensionPoint,
        hash: Hash,
        body: ContractCodeEntryBody,
        expiration_ledger_seq: Uint32,
    ) -> None:
        self.ext = ext
        self.hash = hash
        self.body = body
        self.expiration_ledger_seq = expiration_ledger_seq

    def pack(self, packer: Packer) -> None:
        self.ext.pack(packer)
        self.hash.pack(packer)
        self.body.pack(packer)
        self.expiration_ledger_seq.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ContractCodeEntry:
        ext = ExtensionPoint.unpack(unpacker)
        hash = Hash.unpack(unpacker)
        body = ContractCodeEntryBody.unpack(unpacker)
        expiration_ledger_seq = Uint32.unpack(unpacker)
        return cls(
            ext=ext,
            hash=hash,
            body=body,
            expiration_ledger_seq=expiration_ledger_seq,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ContractCodeEntry:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ContractCodeEntry:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.ext,
                self.hash,
                self.body,
                self.expiration_ledger_seq,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ext == other.ext
            and self.hash == other.hash
            and self.body == other.body
            and self.expiration_ledger_seq == other.expiration_ledger_seq
        )

    def __str__(self):
        out = [
            f"ext={self.ext}",
            f"hash={self.hash}",
            f"body={self.body}",
            f"expiration_ledger_seq={self.expiration_ledger_seq}",
        ]
        return f"<ContractCodeEntry [{', '.join(out)}]>"
