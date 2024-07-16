# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .base import Integer
from .soroban_transaction_data import SorobanTransactionData

__all__ = ["TransactionExt"]


class TransactionExt:
    """
    XDR Source Code::

        union switch (int v)
            {
            case 0:
                void;
            case 1:
                SorobanTransactionData sorobanData;
            }
    """

    def __init__(
        self,
        v: int,
        soroban_data: SorobanTransactionData = None,
    ) -> None:
        self.v = v
        self.soroban_data = soroban_data

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            return
        if self.v == 1:
            if self.soroban_data is None:
                raise ValueError("soroban_data should not be None.")
            self.soroban_data.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> TransactionExt:
        v = Integer.unpack(unpacker)
        if v == 0:
            return cls(v=v)
        if v == 1:
            soroban_data = SorobanTransactionData.unpack(unpacker)
            return cls(v=v, soroban_data=soroban_data)
        return cls(v=v)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TransactionExt:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> TransactionExt:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.v,
                self.soroban_data,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v and self.soroban_data == other.soroban_data

    def __repr__(self):
        out = []
        out.append(f"v={self.v}")
        (
            out.append(f"soroban_data={self.soroban_data}")
            if self.soroban_data is not None
            else None
        )
        return f"<TransactionExt [{', '.join(out)}]>"
