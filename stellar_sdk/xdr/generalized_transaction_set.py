# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .base import Integer
from .transaction_set_v1 import TransactionSetV1

__all__ = ["GeneralizedTransactionSet"]


class GeneralizedTransactionSet:
    """
    XDR Source Code::

        union GeneralizedTransactionSet switch (int v)
        {
        // We consider the legacy TransactionSet to be v0.
        case 1:
            TransactionSetV1 v1TxSet;
        };
    """

    def __init__(
        self,
        v: int,
        v1_tx_set: TransactionSetV1 = None,
    ) -> None:
        self.v = v
        self.v1_tx_set = v1_tx_set

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 1:
            if self.v1_tx_set is None:
                raise ValueError("v1_tx_set should not be None.")
            self.v1_tx_set.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> GeneralizedTransactionSet:
        v = Integer.unpack(unpacker)
        if v == 1:
            v1_tx_set = TransactionSetV1.unpack(unpacker)
            return cls(v=v, v1_tx_set=v1_tx_set)
        return cls(v=v)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> GeneralizedTransactionSet:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> GeneralizedTransactionSet:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.v,
                self.v1_tx_set,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v and self.v1_tx_set == other.v1_tx_set

    def __repr__(self):
        out = []
        out.append(f"v={self.v}")
        (
            out.append(f"v1_tx_set={self.v1_tx_set}")
            if self.v1_tx_set is not None
            else None
        )
        return f"<GeneralizedTransactionSet [{', '.join(out)}]>"
