# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .int64 import Int64
from .uint32 import Uint32

__all__ = ["ConfigSettingContractComputeV0"]


class ConfigSettingContractComputeV0:
    """
    XDR Source Code::

        struct ConfigSettingContractComputeV0
        {
            // Maximum instructions per ledger
            int64 ledgerMaxInstructions;
            // Maximum instructions per transaction
            int64 txMaxInstructions;
            // Cost of 10000 instructions
            int64 feeRatePerInstructionsIncrement;

            // Memory limit per transaction. Unlike instructions, there is no fee
            // for memory, just the limit.
            uint32 txMemoryLimit;
        };
    """

    def __init__(
        self,
        ledger_max_instructions: Int64,
        tx_max_instructions: Int64,
        fee_rate_per_instructions_increment: Int64,
        tx_memory_limit: Uint32,
    ) -> None:
        self.ledger_max_instructions = ledger_max_instructions
        self.tx_max_instructions = tx_max_instructions
        self.fee_rate_per_instructions_increment = fee_rate_per_instructions_increment
        self.tx_memory_limit = tx_memory_limit

    def pack(self, packer: Packer) -> None:
        self.ledger_max_instructions.pack(packer)
        self.tx_max_instructions.pack(packer)
        self.fee_rate_per_instructions_increment.pack(packer)
        self.tx_memory_limit.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ConfigSettingContractComputeV0:
        ledger_max_instructions = Int64.unpack(unpacker)
        tx_max_instructions = Int64.unpack(unpacker)
        fee_rate_per_instructions_increment = Int64.unpack(unpacker)
        tx_memory_limit = Uint32.unpack(unpacker)
        return cls(
            ledger_max_instructions=ledger_max_instructions,
            tx_max_instructions=tx_max_instructions,
            fee_rate_per_instructions_increment=fee_rate_per_instructions_increment,
            tx_memory_limit=tx_memory_limit,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ConfigSettingContractComputeV0:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ConfigSettingContractComputeV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.ledger_max_instructions,
                self.tx_max_instructions,
                self.fee_rate_per_instructions_increment,
                self.tx_memory_limit,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ledger_max_instructions == other.ledger_max_instructions
            and self.tx_max_instructions == other.tx_max_instructions
            and self.fee_rate_per_instructions_increment
            == other.fee_rate_per_instructions_increment
            and self.tx_memory_limit == other.tx_memory_limit
        )

    def __repr__(self):
        out = [
            f"ledger_max_instructions={self.ledger_max_instructions}",
            f"tx_max_instructions={self.tx_max_instructions}",
            f"fee_rate_per_instructions_increment={self.fee_rate_per_instructions_increment}",
            f"tx_memory_limit={self.tx_memory_limit}",
        ]
        return f"<ConfigSettingContractComputeV0 [{', '.join(out)}]>"
