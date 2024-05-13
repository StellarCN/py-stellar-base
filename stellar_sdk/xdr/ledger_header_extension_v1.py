# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .ledger_header_extension_v1_ext import LedgerHeaderExtensionV1Ext
from .uint32 import Uint32

__all__ = ["LedgerHeaderExtensionV1"]


class LedgerHeaderExtensionV1:
    """
    XDR Source Code::

        struct LedgerHeaderExtensionV1
        {
            uint32 flags; // LedgerHeaderFlags

            union switch (int v)
            {
            case 0:
                void;
            }
            ext;
        };
    """

    def __init__(
        self,
        flags: Uint32,
        ext: LedgerHeaderExtensionV1Ext,
    ) -> None:
        self.flags = flags
        self.ext = ext

    def pack(self, packer: Packer) -> None:
        self.flags.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> LedgerHeaderExtensionV1:
        flags = Uint32.unpack(unpacker)
        ext = LedgerHeaderExtensionV1Ext.unpack(unpacker)
        return cls(
            flags=flags,
            ext=ext,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerHeaderExtensionV1:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LedgerHeaderExtensionV1:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.flags,
                self.ext,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.flags == other.flags and self.ext == other.ext

    def __repr__(self):
        out = [
            f"flags={self.flags}",
            f"ext={self.ext}",
        ]
        return f"<LedgerHeaderExtensionV1 [{', '.join(out)}]>"
