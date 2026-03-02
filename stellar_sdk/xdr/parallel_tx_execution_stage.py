# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .dependent_tx_cluster import DependentTxCluster

__all__ = ["ParallelTxExecutionStage"]


class ParallelTxExecutionStage:
    """
    XDR Source Code::

        typedef DependentTxCluster ParallelTxExecutionStage<>;
    """

    def __init__(self, parallel_tx_execution_stage: List[DependentTxCluster]) -> None:
        _expect_max_length = 4294967295
        if (
            parallel_tx_execution_stage
            and len(parallel_tx_execution_stage) > _expect_max_length
        ):
            raise ValueError(
                f"The maximum length of `parallel_tx_execution_stage` should be {_expect_max_length}, but got {len(parallel_tx_execution_stage)}."
            )
        self.parallel_tx_execution_stage = parallel_tx_execution_stage

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.parallel_tx_execution_stage))
        for parallel_tx_execution_stage_item in self.parallel_tx_execution_stage:
            parallel_tx_execution_stage_item.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ParallelTxExecutionStage:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"parallel_tx_execution_stage length {length} exceeds remaining input length {_remaining}"
            )
        parallel_tx_execution_stage = []
        for _ in range(length):
            parallel_tx_execution_stage.append(
                DependentTxCluster.unpack(unpacker, depth_limit - 1)
            )
        return cls(parallel_tx_execution_stage)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ParallelTxExecutionStage:
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
    def from_xdr(cls, xdr: str) -> ParallelTxExecutionStage:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ParallelTxExecutionStage:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        return [item.to_json_dict() for item in self.parallel_tx_execution_stage]

    @classmethod
    def from_json_dict(cls, json_value: list) -> ParallelTxExecutionStage:
        return cls([DependentTxCluster.from_json_dict(item) for item in json_value])

    def __hash__(self):
        return hash((self.parallel_tx_execution_stage,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.parallel_tx_execution_stage == other.parallel_tx_execution_stage

    def __repr__(self):
        return f"<ParallelTxExecutionStage [parallel_tx_execution_stage={self.parallel_tx_execution_stage}]>"
