# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .base import Integer

__all__ = ["LedgerEntryExtensionV1Ext"]


class LedgerEntryExtensionV1Ext:
    """
    XDR Source Code::

        union switch (int v)
            {
            case 0:
                void;
            }
    """

    def __init__(
        self,
        v: int,
    ) -> None:
        self.v = v

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> LedgerEntryExtensionV1Ext:
        v = Integer.unpack(unpacker)
        if v == 0:
            return cls(v=v)
        return cls(v=v)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerEntryExtensionV1Ext:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LedgerEntryExtensionV1Ext:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash((self.v,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v

    def __repr__(self):
        out = []
        out.append(f"v={self.v}")
        return f"<LedgerEntryExtensionV1Ext [{', '.join(out)}]>"
