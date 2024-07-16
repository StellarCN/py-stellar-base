# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .tx_set_component_txs_maybe_discounted_fee import (
    TxSetComponentTxsMaybeDiscountedFee,
)
from .tx_set_component_type import TxSetComponentType

__all__ = ["TxSetComponent"]


class TxSetComponent:
    """
    XDR Source Code::

        union TxSetComponent switch (TxSetComponentType type)
        {
        case TXSET_COMP_TXS_MAYBE_DISCOUNTED_FEE:
          struct
          {
            int64* baseFee;
            TransactionEnvelope txs<>;
          } txsMaybeDiscountedFee;
        };
    """

    def __init__(
        self,
        type: TxSetComponentType,
        txs_maybe_discounted_fee: TxSetComponentTxsMaybeDiscountedFee = None,
    ) -> None:
        self.type = type
        self.txs_maybe_discounted_fee = txs_maybe_discounted_fee

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == TxSetComponentType.TXSET_COMP_TXS_MAYBE_DISCOUNTED_FEE:
            if self.txs_maybe_discounted_fee is None:
                raise ValueError("txs_maybe_discounted_fee should not be None.")
            self.txs_maybe_discounted_fee.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> TxSetComponent:
        type = TxSetComponentType.unpack(unpacker)
        if type == TxSetComponentType.TXSET_COMP_TXS_MAYBE_DISCOUNTED_FEE:
            txs_maybe_discounted_fee = TxSetComponentTxsMaybeDiscountedFee.unpack(
                unpacker
            )
            return cls(type=type, txs_maybe_discounted_fee=txs_maybe_discounted_fee)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TxSetComponent:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> TxSetComponent:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.type,
                self.txs_maybe_discounted_fee,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.txs_maybe_discounted_fee == other.txs_maybe_discounted_fee
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        (
            out.append(f"txs_maybe_discounted_fee={self.txs_maybe_discounted_fee}")
            if self.txs_maybe_discounted_fee is not None
            else None
        )
        return f"<TxSetComponent [{', '.join(out)}]>"
