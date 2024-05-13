# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .hash import Hash

__all__ = ["LedgerKeyTtl"]


class LedgerKeyTtl:
    """
    XDR Source Code::

        struct
            {
                // Hash of the LedgerKey that is associated with this TTLEntry
                Hash keyHash;
            }
    """

    def __init__(
        self,
        key_hash: Hash,
    ) -> None:
        self.key_hash = key_hash

    def pack(self, packer: Packer) -> None:
        self.key_hash.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> LedgerKeyTtl:
        key_hash = Hash.unpack(unpacker)
        return cls(
            key_hash=key_hash,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerKeyTtl:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LedgerKeyTtl:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash((self.key_hash,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.key_hash == other.key_hash

    def __repr__(self):
        out = [
            f"key_hash={self.key_hash}",
        ]
        return f"<LedgerKeyTtl [{', '.join(out)}]>"
