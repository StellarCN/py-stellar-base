# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ConfigSettingContractParallelComputeV0:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        ledger_max_dependent_tx_clusters = Uint32.unpack(unpacker, depth_limit - 1)
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ConfigSettingContractParallelComputeV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ConfigSettingContractParallelComputeV0:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "ledger_max_dependent_tx_clusters": self.ledger_max_dependent_tx_clusters.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> ConfigSettingContractParallelComputeV0:
        ledger_max_dependent_tx_clusters = Uint32.from_json_dict(
            json_dict["ledger_max_dependent_tx_clusters"]
        )
        return cls(
            ledger_max_dependent_tx_clusters=ledger_max_dependent_tx_clusters,
        )

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
