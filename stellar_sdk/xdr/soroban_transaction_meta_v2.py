# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import Optional

from xdrlib3 import Packer, Unpacker

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
    def unpack(cls, unpacker: Unpacker) -> SorobanTransactionMetaV2:
        ext = SorobanTransactionMetaExt.unpack(unpacker)
        return_value = SCVal.unpack(unpacker) if unpacker.unpack_uint() else None
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
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SorobanTransactionMetaV2:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
