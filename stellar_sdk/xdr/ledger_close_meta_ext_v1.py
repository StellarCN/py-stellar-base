# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> LedgerCloseMetaExtV1:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        ext = ExtensionPoint.unpack(unpacker, depth_limit - 1)
        soroban_fee_write1_kb = Int64.unpack(unpacker, depth_limit - 1)
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LedgerCloseMetaExtV1:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LedgerCloseMetaExtV1:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "ext": self.ext.to_json_dict(),
            "soroban_fee_write1_kb": self.soroban_fee_write1_kb.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> LedgerCloseMetaExtV1:
        ext = ExtensionPoint.from_json_dict(json_dict["ext"])
        soroban_fee_write1_kb = Int64.from_json_dict(json_dict["soroban_fee_write1_kb"])
        return cls(
            ext=ext,
            soroban_fee_write1_kb=soroban_fee_write1_kb,
        )

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
