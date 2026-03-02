# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List, Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .int64 import Int64
from .parallel_tx_execution_stage import ParallelTxExecutionStage

__all__ = ["ParallelTxsComponent"]


class ParallelTxsComponent:
    """
    XDR Source Code::

        struct ParallelTxsComponent
        {
          int64* baseFee;
          // A sequence of stages that *may* have arbitrary data dependencies between
          // each other, i.e. in a general case the stage execution order may not be
          // arbitrarily shuffled without affecting the end result.
          ParallelTxExecutionStage executionStages<>;
        };
    """

    def __init__(
        self,
        base_fee: Optional[Int64],
        execution_stages: List[ParallelTxExecutionStage],
    ) -> None:
        _expect_max_length = 4294967295
        if execution_stages and len(execution_stages) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `execution_stages` should be {_expect_max_length}, but got {len(execution_stages)}."
            )
        self.base_fee = base_fee
        self.execution_stages = execution_stages

    def pack(self, packer: Packer) -> None:
        if self.base_fee is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.base_fee.pack(packer)
        packer.pack_uint(len(self.execution_stages))
        for execution_stages_item in self.execution_stages:
            execution_stages_item.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ParallelTxsComponent:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        base_fee = (
            Int64.unpack(unpacker, depth_limit - 1) if unpacker.unpack_uint() else None
        )
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"execution_stages length {length} exceeds remaining input length {_remaining}"
            )
        execution_stages = []
        for _ in range(length):
            execution_stages.append(
                ParallelTxExecutionStage.unpack(unpacker, depth_limit - 1)
            )
        return cls(
            base_fee=base_fee,
            execution_stages=execution_stages,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ParallelTxsComponent:
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
    def from_xdr(cls, xdr: str) -> ParallelTxsComponent:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ParallelTxsComponent:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "base_fee": (
                self.base_fee.to_json_dict() if self.base_fee is not None else None
            ),
            "execution_stages": [item.to_json_dict() for item in self.execution_stages],
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> ParallelTxsComponent:
        base_fee = (
            Int64.from_json_dict(json_dict["base_fee"])
            if json_dict["base_fee"] is not None
            else None
        )
        execution_stages = [
            ParallelTxExecutionStage.from_json_dict(item)
            for item in json_dict["execution_stages"]
        ]
        return cls(
            base_fee=base_fee,
            execution_stages=execution_stages,
        )

    def __hash__(self):
        return hash(
            (
                self.base_fee,
                self.execution_stages,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.base_fee == other.base_fee
            and self.execution_stages == other.execution_stages
        )

    def __repr__(self):
        out = [
            f"base_fee={self.base_fee}",
            f"execution_stages={self.execution_stages}",
        ]
        return f"<ParallelTxsComponent [{', '.join(out)}]>"
