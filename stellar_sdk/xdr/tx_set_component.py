# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
        txs_maybe_discounted_fee: Optional[TxSetComponentTxsMaybeDiscountedFee] = None,
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
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> TxSetComponent:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = TxSetComponentType.unpack(unpacker)
        if type == TxSetComponentType.TXSET_COMP_TXS_MAYBE_DISCOUNTED_FEE:
            txs_maybe_discounted_fee = TxSetComponentTxsMaybeDiscountedFee.unpack(
                unpacker, depth_limit - 1
            )
            return cls(type=type, txs_maybe_discounted_fee=txs_maybe_discounted_fee)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TxSetComponent:
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
    def from_xdr(cls, xdr: str) -> TxSetComponent:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TxSetComponent:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.type == TxSetComponentType.TXSET_COMP_TXS_MAYBE_DISCOUNTED_FEE:
            assert self.txs_maybe_discounted_fee is not None
            return {
                "txset_comp_txs_maybe_discounted_fee": self.txs_maybe_discounted_fee.to_json_dict()
            }
        raise ValueError(f"Unknown type in TxSetComponent: {self.type}")

    @classmethod
    def from_json_dict(cls, json_value: dict) -> TxSetComponent:
        if len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for TxSetComponent, got: {json_value}"
            )
        key = next(iter(json_value))
        type = TxSetComponentType.from_json_dict(key)
        if key == "txset_comp_txs_maybe_discounted_fee":
            txs_maybe_discounted_fee = (
                TxSetComponentTxsMaybeDiscountedFee.from_json_dict(
                    json_value["txset_comp_txs_maybe_discounted_fee"]
                )
            )
            return cls(type=type, txs_maybe_discounted_fee=txs_maybe_discounted_fee)
        raise ValueError(f"Unknown key '{key}' for TxSetComponent")

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
        if self.txs_maybe_discounted_fee is not None:
            out.append(f"txs_maybe_discounted_fee={self.txs_maybe_discounted_fee}")
        return f"<TxSetComponent [{', '.join(out)}]>"
