# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .int64 import Int64
from .uint32 import Uint32

__all__ = ["ConfigSettingContractEventsV0"]


class ConfigSettingContractEventsV0:
    """
    XDR Source Code::

        struct ConfigSettingContractEventsV0
        {
            // Maximum size of events that a contract call can emit.
            uint32 txMaxContractEventsSizeBytes;
            // Fee for generating 1KB of contract events.
            int64 feeContractEvents1KB;
        };
    """

    def __init__(
        self,
        tx_max_contract_events_size_bytes: Uint32,
        fee_contract_events1_kb: Int64,
    ) -> None:
        self.tx_max_contract_events_size_bytes = tx_max_contract_events_size_bytes
        self.fee_contract_events1_kb = fee_contract_events1_kb

    def pack(self, packer: Packer) -> None:
        self.tx_max_contract_events_size_bytes.pack(packer)
        self.fee_contract_events1_kb.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ConfigSettingContractEventsV0:
        tx_max_contract_events_size_bytes = Uint32.unpack(unpacker)
        fee_contract_events1_kb = Int64.unpack(unpacker)
        return cls(
            tx_max_contract_events_size_bytes=tx_max_contract_events_size_bytes,
            fee_contract_events1_kb=fee_contract_events1_kb,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ConfigSettingContractEventsV0:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ConfigSettingContractEventsV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.tx_max_contract_events_size_bytes,
                self.fee_contract_events1_kb,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.tx_max_contract_events_size_bytes
            == other.tx_max_contract_events_size_bytes
            and self.fee_contract_events1_kb == other.fee_contract_events1_kb
        )

    def __repr__(self):
        out = [
            f"tx_max_contract_events_size_bytes={self.tx_max_contract_events_size_bytes}",
            f"fee_contract_events1_kb={self.fee_contract_events1_kb}",
        ]
        return f"<ConfigSettingContractEventsV0 [{', '.join(out)}]>"
