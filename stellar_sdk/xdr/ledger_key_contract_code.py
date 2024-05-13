# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .hash import Hash

__all__ = ["LedgerKeyContractCode"]


class LedgerKeyContractCode:
    """
    XDR Source Code::

        struct
            {
                Hash hash;
            }
    """

    def __init__(
        self,
        hash: Hash,
    ) -> None:
        self.hash = hash

    def pack(self, packer: Packer) -> None:
        self.hash.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> LedgerKeyContractCode:
        hash = Hash.unpack(unpacker)
        return cls(
            hash=hash,
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
        return hash((self.hash,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.hash == other.hash

    def __repr__(self):
        out = [
            f"hash={self.hash}",
        ]
        return f"<LedgerKeyContractCode [{', '.join(out)}]>"
