# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> TrustLineEntryExtensionV2:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        liquidity_pool_use_count = Int32.unpack(unpacker, depth_limit - 1)
        ext = TrustLineEntryExtensionV2Ext.unpack(unpacker, depth_limit - 1)
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> TrustLineEntryExtensionV2:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TrustLineEntryExtensionV2:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "liquidity_pool_use_count": self.liquidity_pool_use_count.to_json_dict(),
            "ext": self.ext.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> TrustLineEntryExtensionV2:
        liquidity_pool_use_count = Int32.from_json_dict(
            json_dict["liquidity_pool_use_count"]
        )
        ext = TrustLineEntryExtensionV2Ext.from_json_dict(json_dict["ext"])
        return cls(
            liquidity_pool_use_count=liquidity_pool_use_count,
            ext=ext,
        )

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
