# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ConfigSettingContractEventsV0:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        tx_max_contract_events_size_bytes = Uint32.unpack(unpacker, depth_limit - 1)
        fee_contract_events1_kb = Int64.unpack(unpacker, depth_limit - 1)
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ConfigSettingContractEventsV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ConfigSettingContractEventsV0:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "tx_max_contract_events_size_bytes": self.tx_max_contract_events_size_bytes.to_json_dict(),
            "fee_contract_events1_kb": self.fee_contract_events1_kb.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> ConfigSettingContractEventsV0:
        tx_max_contract_events_size_bytes = Uint32.from_json_dict(
            json_dict["tx_max_contract_events_size_bytes"]
        )
        fee_contract_events1_kb = Int64.from_json_dict(
            json_dict["fee_contract_events1_kb"]
        )
        return cls(
            tx_max_contract_events_size_bytes=tx_max_contract_events_size_bytes,
            fee_contract_events1_kb=fee_contract_events1_kb,
        )

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
