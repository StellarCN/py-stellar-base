# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .constants import *
from .hash import Hash

__all__ = ["TxDemandVector"]


class TxDemandVector:
    """
    XDR Source Code::

        typedef Hash TxDemandVector<TX_DEMAND_VECTOR_MAX_SIZE>;
    """

    def __init__(self, tx_demand_vector: List[Hash]) -> None:
        _expect_max_length = TX_DEMAND_VECTOR_MAX_SIZE
        if tx_demand_vector and len(tx_demand_vector) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `tx_demand_vector` should be {_expect_max_length}, but got {len(tx_demand_vector)}."
            )
        self.tx_demand_vector = tx_demand_vector

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.tx_demand_vector))
        for tx_demand_vector_item in self.tx_demand_vector:
            tx_demand_vector_item.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> TxDemandVector:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"tx_demand_vector length {length} exceeds remaining input length {_remaining}"
            )
        tx_demand_vector = []
        for _ in range(length):
            tx_demand_vector.append(Hash.unpack(unpacker, depth_limit - 1))
        return cls(tx_demand_vector)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TxDemandVector:
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
    def from_xdr(cls, xdr: str) -> TxDemandVector:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TxDemandVector:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        return [item.to_json_dict() for item in self.tx_demand_vector]

    @classmethod
    def from_json_dict(cls, json_value: list) -> TxDemandVector:
        return cls([Hash.from_json_dict(item) for item in json_value])

    def __hash__(self):
        return hash((self.tx_demand_vector,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.tx_demand_vector == other.tx_demand_vector

    def __repr__(self):
        return f"<TxDemandVector [tx_demand_vector={self.tx_demand_vector}]>"
