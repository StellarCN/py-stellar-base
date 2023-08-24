# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .contract_entry_body_type import ContractEntryBodyType
from .hash import Hash

__all__ = ["LedgerKeyContractCode"]


class LedgerKeyContractCode:
    """
    XDR Source Code::

        struct
            {
                Hash hash;
                ContractEntryBodyType bodyType;
            }
    """

    def __init__(
        self,
        hash: Hash,
        body_type: ContractEntryBodyType,
    ) -> None:
        self.hash = hash
        self.body_type = body_type

    def pack(self, packer: Packer) -> None:
        self.hash.pack(packer)
        self.body_type.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> LedgerKeyContractCode:
        hash = Hash.unpack(unpacker)
        body_type = ContractEntryBodyType.unpack(unpacker)
        return cls(
            hash=hash,
            body_type=body_type,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerKeyContractCode:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LedgerKeyContractCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.hash,
                self.body_type,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.hash == other.hash and self.body_type == other.body_type

    def __str__(self):
        out = [
            f"hash={self.hash}",
            f"body_type={self.body_type}",
        ]
        return f"<LedgerKeyContractCode [{', '.join(out)}]>"
