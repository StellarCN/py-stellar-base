# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List, Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> TxSetComponentTxsMaybeDiscountedFee:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        base_fee = (
            Int64.unpack(unpacker, depth_limit - 1) if unpacker.unpack_uint() else None
        )
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"txs length {length} exceeds remaining input length {_remaining}"
            )
        txs = []
        for _ in range(length):
            txs.append(TransactionEnvelope.unpack(unpacker, depth_limit - 1))
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> TxSetComponentTxsMaybeDiscountedFee:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TxSetComponentTxsMaybeDiscountedFee:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "base_fee": (
                self.base_fee.to_json_dict() if self.base_fee is not None else None
            ),
            "txs": [item.to_json_dict() for item in self.txs],
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> TxSetComponentTxsMaybeDiscountedFee:
        base_fee = (
            Int64.from_json_dict(json_dict["base_fee"])
            if json_dict["base_fee"] is not None
            else None
        )
        txs = [TransactionEnvelope.from_json_dict(item) for item in json_dict["txs"]]
        return cls(
            base_fee=base_fee,
            txs=txs,
        )

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
