# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .uint32 import Uint32

__all__ = ["ConfigSettingContractParallelComputeV0"]


class ConfigSettingContractParallelComputeV0:
    """
    XDR Source Code::

        struct ConfigSettingContractParallelComputeV0
        {
            // Maximum number of clusters with dependent transactions allowed in a
            // stage of parallel tx set component.
            // This effectively sets the lower bound on the number of physical threads
            // necessary to effectively apply transaction sets in parallel.
            uint32 ledgerMaxDependentTxClusters;
        };
    """

    def __init__(
        self,
        ledger_max_dependent_tx_clusters: Uint32,
    ) -> None:
        self.ledger_max_dependent_tx_clusters = ledger_max_dependent_tx_clusters

    def pack(self, packer: Packer) -> None:
        self.ledger_max_dependent_tx_clusters.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ConfigSettingContractParallelComputeV0:
        ledger_max_dependent_tx_clusters = Uint32.unpack(unpacker)
        return cls(
            ledger_max_dependent_tx_clusters=ledger_max_dependent_tx_clusters,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ConfigSettingContractParallelComputeV0:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ConfigSettingContractParallelComputeV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash((self.ledger_max_dependent_tx_clusters,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ledger_max_dependent_tx_clusters
            == other.ledger_max_dependent_tx_clusters
        )

    def __repr__(self):
        out = [
            f"ledger_max_dependent_tx_clusters={self.ledger_max_dependent_tx_clusters}",
        ]
        return f"<ConfigSettingContractParallelComputeV0 [{', '.join(out)}]>"
