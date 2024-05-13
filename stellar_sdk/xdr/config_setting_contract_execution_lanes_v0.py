# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .uint32 import Uint32

__all__ = ["ConfigSettingContractExecutionLanesV0"]


class ConfigSettingContractExecutionLanesV0:
    """
    XDR Source Code::

        struct ConfigSettingContractExecutionLanesV0
        {
            // maximum number of Soroban transactions per ledger
            uint32 ledgerMaxTxCount;
        };
    """

    def __init__(
        self,
        ledger_max_tx_count: Uint32,
    ) -> None:
        self.ledger_max_tx_count = ledger_max_tx_count

    def pack(self, packer: Packer) -> None:
        self.ledger_max_tx_count.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ConfigSettingContractExecutionLanesV0:
        ledger_max_tx_count = Uint32.unpack(unpacker)
        return cls(
            ledger_max_tx_count=ledger_max_tx_count,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ConfigSettingContractExecutionLanesV0:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ConfigSettingContractExecutionLanesV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash((self.ledger_max_tx_count,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.ledger_max_tx_count == other.ledger_max_tx_count

    def __repr__(self):
        out = [
            f"ledger_max_tx_count={self.ledger_max_tx_count}",
        ]
        return f"<ConfigSettingContractExecutionLanesV0 [{', '.join(out)}]>"
