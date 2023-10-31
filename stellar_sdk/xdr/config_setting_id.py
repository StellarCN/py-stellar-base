# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

__all__ = ["ConfigSettingID"]


class ConfigSettingID(IntEnum):
    """
    XDR Source Code::

        enum ConfigSettingID
        {
            CONFIG_SETTING_CONTRACT_MAX_SIZE_BYTES = 0,
            CONFIG_SETTING_CONTRACT_COMPUTE_V0 = 1,
            CONFIG_SETTING_CONTRACT_LEDGER_COST_V0 = 2,
            CONFIG_SETTING_CONTRACT_HISTORICAL_DATA_V0 = 3,
            CONFIG_SETTING_CONTRACT_EVENTS_V0 = 4,
            CONFIG_SETTING_CONTRACT_BANDWIDTH_V0 = 5,
            CONFIG_SETTING_CONTRACT_COST_PARAMS_CPU_INSTRUCTIONS = 6,
            CONFIG_SETTING_CONTRACT_COST_PARAMS_MEMORY_BYTES = 7,
            CONFIG_SETTING_CONTRACT_DATA_KEY_SIZE_BYTES = 8,
            CONFIG_SETTING_CONTRACT_DATA_ENTRY_SIZE_BYTES = 9,
            CONFIG_SETTING_STATE_ARCHIVAL = 10,
            CONFIG_SETTING_CONTRACT_EXECUTION_LANES = 11,
            CONFIG_SETTING_BUCKETLIST_SIZE_WINDOW = 12,
            CONFIG_SETTING_EVICTION_ITERATOR = 13
        };
    """

    CONFIG_SETTING_CONTRACT_MAX_SIZE_BYTES = 0
    CONFIG_SETTING_CONTRACT_COMPUTE_V0 = 1
    CONFIG_SETTING_CONTRACT_LEDGER_COST_V0 = 2
    CONFIG_SETTING_CONTRACT_HISTORICAL_DATA_V0 = 3
    CONFIG_SETTING_CONTRACT_EVENTS_V0 = 4
    CONFIG_SETTING_CONTRACT_BANDWIDTH_V0 = 5
    CONFIG_SETTING_CONTRACT_COST_PARAMS_CPU_INSTRUCTIONS = 6
    CONFIG_SETTING_CONTRACT_COST_PARAMS_MEMORY_BYTES = 7
    CONFIG_SETTING_CONTRACT_DATA_KEY_SIZE_BYTES = 8
    CONFIG_SETTING_CONTRACT_DATA_ENTRY_SIZE_BYTES = 9
    CONFIG_SETTING_STATE_ARCHIVAL = 10
    CONFIG_SETTING_CONTRACT_EXECUTION_LANES = 11
    CONFIG_SETTING_BUCKETLIST_SIZE_WINDOW = 12
    CONFIG_SETTING_EVICTION_ITERATOR = 13

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ConfigSettingID:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ConfigSettingID:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ConfigSettingID:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
