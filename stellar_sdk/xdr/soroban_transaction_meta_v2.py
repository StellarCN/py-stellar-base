# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .sc_val import SCVal
from .soroban_transaction_meta_ext import SorobanTransactionMetaExt

__all__ = ["SorobanTransactionMetaV2"]


class SorobanTransactionMetaV2:
    """
    XDR Source Code::

        struct SorobanTransactionMetaV2
        {
            SorobanTransactionMetaExt ext;

            SCVal* returnValue;
        };
    """

    def __init__(
        self,
        ext: SorobanTransactionMetaExt,
        return_value: Optional[SCVal],
    ) -> None:
        self.ext = ext
        self.return_value = return_value

    def pack(self, packer: Packer) -> None:
        self.ext.pack(packer)
        if self.return_value is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.return_value.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SorobanTransactionMetaV2:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        ext = SorobanTransactionMetaExt.unpack(unpacker, depth_limit - 1)
        return_value = (
            SCVal.unpack(unpacker, depth_limit - 1) if unpacker.unpack_uint() else None
        )
        return cls(
            ext=ext,
            return_value=return_value,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SorobanTransactionMetaV2:
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
    def from_xdr(cls, xdr: str) -> SorobanTransactionMetaV2:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SorobanTransactionMetaV2:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "ext": self.ext.to_json_dict(),
            "return_value": (
                self.return_value.to_json_dict()
                if self.return_value is not None
                else None
            ),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SorobanTransactionMetaV2:
        ext = SorobanTransactionMetaExt.from_json_dict(json_dict["ext"])
        return_value = (
            SCVal.from_json_dict(json_dict["return_value"])
            if json_dict["return_value"] is not None
            else None
        )
        return cls(
            ext=ext,
            return_value=return_value,
        )

    def __hash__(self):
        return hash(
            (
                self.ext,
                self.return_value,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.ext == other.ext and self.return_value == other.return_value

    def __repr__(self):
        out = [
            f"ext={self.ext}",
            f"return_value={self.return_value}",
        ]
        return f"<SorobanTransactionMetaV2 [{', '.join(out)}]>"
