# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_TX_SET_COMPONENT_TYPE_MAP = {0: "txset_comp_txs_maybe_discounted_fee"}
_TX_SET_COMPONENT_TYPE_REVERSE_MAP = {"txset_comp_txs_maybe_discounted_fee": 0}
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> TxSetComponentType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TxSetComponentType:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _TX_SET_COMPONENT_TYPE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> TxSetComponentType:
        return cls(_TX_SET_COMPONENT_TYPE_REVERSE_MAP[json_value])
