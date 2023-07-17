# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

__all__ = ["TxSetComponentType"]


class TxSetComponentType(IntEnum):
    """
    XDR Source Code::

        enum TxSetComponentType
        {
          // txs with effective fee <= bid derived from a base fee (if any).
          // If base fee is not specified, no discount is applied.
          TXSET_COMP_TXS_MAYBE_DISCOUNTED_FEE = 0
        };
    """

    TXSET_COMP_TXS_MAYBE_DISCOUNTED_FEE = 0

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> TxSetComponentType:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TxSetComponentType:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> TxSetComponentType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
