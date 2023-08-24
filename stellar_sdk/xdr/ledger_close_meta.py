# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .base import Integer
from .ledger_close_meta_v0 import LedgerCloseMetaV0
from .ledger_close_meta_v1 import LedgerCloseMetaV1
from .ledger_close_meta_v2 import LedgerCloseMetaV2

__all__ = ["LedgerCloseMeta"]


class LedgerCloseMeta:
    """
    XDR Source Code::

        union LedgerCloseMeta switch (int v)
        {
        case 0:
            LedgerCloseMetaV0 v0;
        case 1:
            LedgerCloseMetaV1 v1;
        case 2:
            LedgerCloseMetaV2 v2;
        };
    """

    def __init__(
        self,
        v: int,
        v0: LedgerCloseMetaV0 = None,
        v1: LedgerCloseMetaV1 = None,
        v2: LedgerCloseMetaV2 = None,
    ) -> None:
        self.v = v
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            if self.v0 is None:
                raise ValueError("v0 should not be None.")
            self.v0.pack(packer)
            return
        if self.v == 1:
            if self.v1 is None:
                raise ValueError("v1 should not be None.")
            self.v1.pack(packer)
            return
        if self.v == 2:
            if self.v2 is None:
                raise ValueError("v2 should not be None.")
            self.v2.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> LedgerCloseMeta:
        v = Integer.unpack(unpacker)
        if v == 0:
            v0 = LedgerCloseMetaV0.unpack(unpacker)
            return cls(v=v, v0=v0)
        if v == 1:
            v1 = LedgerCloseMetaV1.unpack(unpacker)
            return cls(v=v, v1=v1)
        if v == 2:
            v2 = LedgerCloseMetaV2.unpack(unpacker)
            return cls(v=v, v2=v2)
        return cls(v=v)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerCloseMeta:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LedgerCloseMeta:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.v,
                self.v0,
                self.v1,
                self.v2,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.v == other.v
            and self.v0 == other.v0
            and self.v1 == other.v1
            and self.v2 == other.v2
        )

    def __str__(self):
        out = []
        out.append(f"v={self.v}")
        out.append(f"v0={self.v0}") if self.v0 is not None else None
        out.append(f"v1={self.v1}") if self.v1 is not None else None
        out.append(f"v2={self.v2}") if self.v2 is not None else None
        return f"<LedgerCloseMeta [{', '.join(out)}]>"
