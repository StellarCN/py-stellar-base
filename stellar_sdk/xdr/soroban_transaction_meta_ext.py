# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .base import Integer
from .soroban_transaction_meta_ext_v1 import SorobanTransactionMetaExtV1

__all__ = ["SorobanTransactionMetaExt"]


class SorobanTransactionMetaExt:
    """
    XDR Source Code::

        union SorobanTransactionMetaExt switch (int v)
        {
        case 0:
            void;
        case 1:
            SorobanTransactionMetaExtV1 v1;
        };
    """

    def __init__(
        self,
        v: int,
        v1: SorobanTransactionMetaExtV1 = None,
    ) -> None:
        self.v = v
        self.v1 = v1

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            return
        if self.v == 1:
            if self.v1 is None:
                raise ValueError("v1 should not be None.")
            self.v1.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SorobanTransactionMetaExt:
        v = Integer.unpack(unpacker)
        if v == 0:
            return cls(v=v)
        if v == 1:
            v1 = SorobanTransactionMetaExtV1.unpack(unpacker)
            return cls(v=v, v1=v1)
        return cls(v=v)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SorobanTransactionMetaExt:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SorobanTransactionMetaExt:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.v,
                self.v1,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v and self.v1 == other.v1

    def __repr__(self):
        out = []
        out.append(f"v={self.v}")
        out.append(f"v1={self.v1}") if self.v1 is not None else None
        return f"<SorobanTransactionMetaExt [{', '.join(out)}]>"
