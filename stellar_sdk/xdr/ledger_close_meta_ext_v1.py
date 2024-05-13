# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .extension_point import ExtensionPoint
from .int64 import Int64

__all__ = ["LedgerCloseMetaExtV1"]


class LedgerCloseMetaExtV1:
    """
    XDR Source Code::

        struct LedgerCloseMetaExtV1
        {
            ExtensionPoint ext;
            int64 sorobanFeeWrite1KB;
        };
    """

    def __init__(
        self,
        ext: ExtensionPoint,
        soroban_fee_write1_kb: Int64,
    ) -> None:
        self.ext = ext
        self.soroban_fee_write1_kb = soroban_fee_write1_kb

    def pack(self, packer: Packer) -> None:
        self.ext.pack(packer)
        self.soroban_fee_write1_kb.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> LedgerCloseMetaExtV1:
        ext = ExtensionPoint.unpack(unpacker)
        soroban_fee_write1_kb = Int64.unpack(unpacker)
        return cls(
            ext=ext,
            soroban_fee_write1_kb=soroban_fee_write1_kb,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerCloseMetaExtV1:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LedgerCloseMetaExtV1:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.ext,
                self.soroban_fee_write1_kb,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ext == other.ext
            and self.soroban_fee_write1_kb == other.soroban_fee_write1_kb
        )

    def __repr__(self):
        out = [
            f"ext={self.ext}",
            f"soroban_fee_write1_kb={self.soroban_fee_write1_kb}",
        ]
        return f"<LedgerCloseMetaExtV1 [{', '.join(out)}]>"
