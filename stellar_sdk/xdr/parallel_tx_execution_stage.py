# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

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
    def unpack(cls, unpacker: Unpacker) -> ParallelTxExecutionStage:
        length = unpacker.unpack_uint()
        parallel_tx_execution_stage = []
        for _ in range(length):
            parallel_tx_execution_stage.append(DependentTxCluster.unpack(unpacker))
        return cls(parallel_tx_execution_stage)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ParallelTxExecutionStage:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ParallelTxExecutionStage:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(self.parallel_tx_execution_stage)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.parallel_tx_execution_stage == other.parallel_tx_execution_stage

    def __repr__(self):
        return f"<ParallelTxExecutionStage [parallel_tx_execution_stage={self.parallel_tx_execution_stage}]>"
