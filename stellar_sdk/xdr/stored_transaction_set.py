# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .base import Integer
from .generalized_transaction_set import GeneralizedTransactionSet
from .transaction_set import TransactionSet

__all__ = ["StoredTransactionSet"]


class StoredTransactionSet:
    """
    XDR Source Code::

                                                                union StoredTransactionSet switch (int v)
                                                                {
                                                                case 0:
                                                                        TransactionSet txSet;
                                                                case 1:
                                                                        GeneralizedTransactionSet generalizedTxSet;
                                                                };
    """

    def __init__(
        self,
        v: int,
        tx_set: TransactionSet = None,
        generalized_tx_set: GeneralizedTransactionSet = None,
    ) -> None:
        self.v = v
        self.tx_set = tx_set
        self.generalized_tx_set = generalized_tx_set

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            if self.tx_set is None:
                raise ValueError("tx_set should not be None.")
            self.tx_set.pack(packer)
            return
        if self.v == 1:
            if self.generalized_tx_set is None:
                raise ValueError("generalized_tx_set should not be None.")
            self.generalized_tx_set.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> StoredTransactionSet:
        v = Integer.unpack(unpacker)
        if v == 0:
            tx_set = TransactionSet.unpack(unpacker)
            return cls(v=v, tx_set=tx_set)
        if v == 1:
            generalized_tx_set = GeneralizedTransactionSet.unpack(unpacker)
            return cls(v=v, generalized_tx_set=generalized_tx_set)
        return cls(v=v)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> StoredTransactionSet:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> StoredTransactionSet:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.v,
                self.tx_set,
                self.generalized_tx_set,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.v == other.v
            and self.tx_set == other.tx_set
            and self.generalized_tx_set == other.generalized_tx_set
        )

    def __repr__(self):
        out = []
        out.append(f"v={self.v}")
        out.append(f"tx_set={self.tx_set}") if self.tx_set is not None else None
        (
            out.append(f"generalized_tx_set={self.generalized_tx_set}")
            if self.generalized_tx_set is not None
            else None
        )
        return f"<StoredTransactionSet [{', '.join(out)}]>"
