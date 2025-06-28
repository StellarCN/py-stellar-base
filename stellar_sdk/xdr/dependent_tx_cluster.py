# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

from .transaction_envelope import TransactionEnvelope

__all__ = ["DependentTxCluster"]


class DependentTxCluster:
    """
    XDR Source Code::

        typedef TransactionEnvelope DependentTxCluster<>;
    """

    def __init__(self, dependent_tx_cluster: List[TransactionEnvelope]) -> None:
        _expect_max_length = 4294967295
        if dependent_tx_cluster and len(dependent_tx_cluster) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `dependent_tx_cluster` should be {_expect_max_length}, but got {len(dependent_tx_cluster)}."
            )
        self.dependent_tx_cluster = dependent_tx_cluster

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.dependent_tx_cluster))
        for dependent_tx_cluster_item in self.dependent_tx_cluster:
            dependent_tx_cluster_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> DependentTxCluster:
        length = unpacker.unpack_uint()
        dependent_tx_cluster = []
        for _ in range(length):
            dependent_tx_cluster.append(TransactionEnvelope.unpack(unpacker))
        return cls(dependent_tx_cluster)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> DependentTxCluster:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> DependentTxCluster:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(self.dependent_tx_cluster)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.dependent_tx_cluster == other.dependent_tx_cluster

    def __repr__(self):
        return (
            f"<DependentTxCluster [dependent_tx_cluster={self.dependent_tx_cluster}]>"
        )
