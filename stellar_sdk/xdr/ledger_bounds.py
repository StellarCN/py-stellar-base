# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .uint32 import Uint32

__all__ = ["LedgerBounds"]


class LedgerBounds:
    """
    XDR Source Code::

        struct LedgerBounds
        {
            uint32 minLedger;
            uint32 maxLedger; // 0 here means no maxLedger
        };
    """

    def __init__(
        self,
        min_ledger: Uint32,
        max_ledger: Uint32,
    ) -> None:
        self.min_ledger = min_ledger
        self.max_ledger = max_ledger

    def pack(self, packer: Packer) -> None:
        self.min_ledger.pack(packer)
        self.max_ledger.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> LedgerBounds:
        min_ledger = Uint32.unpack(unpacker)
        max_ledger = Uint32.unpack(unpacker)
        return cls(
            min_ledger=min_ledger,
            max_ledger=max_ledger,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerBounds:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LedgerBounds:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.min_ledger,
                self.max_ledger,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.min_ledger == other.min_ledger and self.max_ledger == other.max_ledger
        )

    def __repr__(self):
        out = [
            f"min_ledger={self.min_ledger}",
            f"max_ledger={self.max_ledger}",
        ]
        return f"<LedgerBounds [{', '.join(out)}]>"
