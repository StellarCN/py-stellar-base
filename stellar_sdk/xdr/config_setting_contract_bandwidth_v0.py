# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .int64 import Int64
from .uint32 import Uint32

__all__ = ["ConfigSettingContractBandwidthV0"]


class ConfigSettingContractBandwidthV0:
    """
    XDR Source Code::

        struct ConfigSettingContractBandwidthV0
        {
            // Maximum sum of all transaction sizes in the ledger in bytes
            uint32 ledgerMaxTxsSizeBytes;
            // Maximum size in bytes for a transaction
            uint32 txMaxSizeBytes;

            // Fee for 1 KB of transaction size
            int64 feeTxSize1KB;
        };
    """

    def __init__(
        self,
        ledger_max_txs_size_bytes: Uint32,
        tx_max_size_bytes: Uint32,
        fee_tx_size1_kb: Int64,
    ) -> None:
        self.ledger_max_txs_size_bytes = ledger_max_txs_size_bytes
        self.tx_max_size_bytes = tx_max_size_bytes
        self.fee_tx_size1_kb = fee_tx_size1_kb

    def pack(self, packer: Packer) -> None:
        self.ledger_max_txs_size_bytes.pack(packer)
        self.tx_max_size_bytes.pack(packer)
        self.fee_tx_size1_kb.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ConfigSettingContractBandwidthV0:
        ledger_max_txs_size_bytes = Uint32.unpack(unpacker)
        tx_max_size_bytes = Uint32.unpack(unpacker)
        fee_tx_size1_kb = Int64.unpack(unpacker)
        return cls(
            ledger_max_txs_size_bytes=ledger_max_txs_size_bytes,
            tx_max_size_bytes=tx_max_size_bytes,
            fee_tx_size1_kb=fee_tx_size1_kb,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ConfigSettingContractBandwidthV0:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ConfigSettingContractBandwidthV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.ledger_max_txs_size_bytes,
                self.tx_max_size_bytes,
                self.fee_tx_size1_kb,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ledger_max_txs_size_bytes == other.ledger_max_txs_size_bytes
            and self.tx_max_size_bytes == other.tx_max_size_bytes
            and self.fee_tx_size1_kb == other.fee_tx_size1_kb
        )

    def __repr__(self):
        out = [
            f"ledger_max_txs_size_bytes={self.ledger_max_txs_size_bytes}",
            f"tx_max_size_bytes={self.tx_max_size_bytes}",
            f"fee_tx_size1_kb={self.fee_tx_size1_kb}",
        ]
        return f"<ConfigSettingContractBandwidthV0 [{', '.join(out)}]>"
