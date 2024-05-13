# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List, Optional

from xdrlib3 import Packer, Unpacker

from .int64 import Int64
from .transaction_envelope import TransactionEnvelope

__all__ = ["TxSetComponentTxsMaybeDiscountedFee"]


class TxSetComponentTxsMaybeDiscountedFee:
    """
    XDR Source Code::

        struct
          {
            int64* baseFee;
            TransactionEnvelope txs<>;
          }
    """

    def __init__(
        self,
        base_fee: Optional[Int64],
        txs: List[TransactionEnvelope],
    ) -> None:
        _expect_max_length = 4294967295
        if txs and len(txs) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `txs` should be {_expect_max_length}, but got {len(txs)}."
            )
        self.base_fee = base_fee
        self.txs = txs

    def pack(self, packer: Packer) -> None:
        if self.base_fee is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.base_fee.pack(packer)
        packer.pack_uint(len(self.txs))
        for txs_item in self.txs:
            txs_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> TxSetComponentTxsMaybeDiscountedFee:
        base_fee = Int64.unpack(unpacker) if unpacker.unpack_uint() else None
        length = unpacker.unpack_uint()
        txs = []
        for _ in range(length):
            txs.append(TransactionEnvelope.unpack(unpacker))
        return cls(
            base_fee=base_fee,
            txs=txs,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TxSetComponentTxsMaybeDiscountedFee:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> TxSetComponentTxsMaybeDiscountedFee:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.base_fee,
                self.txs,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.base_fee == other.base_fee and self.txs == other.txs

    def __repr__(self):
        out = [
            f"base_fee={self.base_fee}",
            f"txs={self.txs}",
        ]
        return f"<TxSetComponentTxsMaybeDiscountedFee [{', '.join(out)}]>"
