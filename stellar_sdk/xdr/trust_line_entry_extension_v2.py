# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .int32 import Int32
from .trust_line_entry_extension_v2_ext import TrustLineEntryExtensionV2Ext

__all__ = ["TrustLineEntryExtensionV2"]


class TrustLineEntryExtensionV2:
    """
    XDR Source Code::

        struct TrustLineEntryExtensionV2
        {
            int32 liquidityPoolUseCount;

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
        liquidity_pool_use_count: Int32,
        ext: TrustLineEntryExtensionV2Ext,
    ) -> None:
        self.liquidity_pool_use_count = liquidity_pool_use_count
        self.ext = ext

    def pack(self, packer: Packer) -> None:
        self.liquidity_pool_use_count.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> TrustLineEntryExtensionV2:
        liquidity_pool_use_count = Int32.unpack(unpacker)
        ext = TrustLineEntryExtensionV2Ext.unpack(unpacker)
        return cls(
            liquidity_pool_use_count=liquidity_pool_use_count,
            ext=ext,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TrustLineEntryExtensionV2:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> TrustLineEntryExtensionV2:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.liquidity_pool_use_count,
                self.ext,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.liquidity_pool_use_count == other.liquidity_pool_use_count
            and self.ext == other.ext
        )

    def __repr__(self):
        out = [
            f"liquidity_pool_use_count={self.liquidity_pool_use_count}",
            f"ext={self.ext}",
        ]
        return f"<TrustLineEntryExtensionV2 [{', '.join(out)}]>"
