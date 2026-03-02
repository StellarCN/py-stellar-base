# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_CONFIG_SETTING_ID_MAP = {
    0: "contract_max_size_bytes",
    1: "contract_compute_v0",
    2: "contract_ledger_cost_v0",
    3: "contract_historical_data_v0",
    4: "contract_events_v0",
    5: "contract_bandwidth_v0",
    6: "contract_cost_params_cpu_instructions",
    7: "contract_cost_params_memory_bytes",
    8: "contract_data_key_size_bytes",
    9: "contract_data_entry_size_bytes",
    10: "state_archival",
    11: "contract_execution_lanes",
    12: "live_soroban_state_size_window",
    13: "eviction_iterator",
    14: "contract_parallel_compute_v0",
    15: "contract_ledger_cost_ext_v0",
    16: "scp_timing",
}
_CONFIG_SETTING_ID_REVERSE_MAP = {
    "contract_max_size_bytes": 0,
    "contract_compute_v0": 1,
    "contract_ledger_cost_v0": 2,
    "contract_historical_data_v0": 3,
    "contract_events_v0": 4,
    "contract_bandwidth_v0": 5,
    "contract_cost_params_cpu_instructions": 6,
    "contract_cost_params_memory_bytes": 7,
    "contract_data_key_size_bytes": 8,
    "contract_data_entry_size_bytes": 9,
    "state_archival": 10,
    "contract_execution_lanes": 11,
    "live_soroban_state_size_window": 12,
    "eviction_iterator": 13,
    "contract_parallel_compute_v0": 14,
    "contract_ledger_cost_ext_v0": 15,
    "scp_timing": 16,
}
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
            CONFIG_SETTING_LIVE_SOROBAN_STATE_SIZE_WINDOW = 12,
            CONFIG_SETTING_EVICTION_ITERATOR = 13,
            CONFIG_SETTING_CONTRACT_PARALLEL_COMPUTE_V0 = 14,
            CONFIG_SETTING_CONTRACT_LEDGER_COST_EXT_V0 = 15,
            CONFIG_SETTING_SCP_TIMING = 16
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
    CONFIG_SETTING_LIVE_SOROBAN_STATE_SIZE_WINDOW = 12
    CONFIG_SETTING_EVICTION_ITERATOR = 13
    CONFIG_SETTING_CONTRACT_PARALLEL_COMPUTE_V0 = 14
    CONFIG_SETTING_CONTRACT_LEDGER_COST_EXT_V0 = 15
    CONFIG_SETTING_SCP_TIMING = 16

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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ConfigSettingID:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ConfigSettingID:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _CONFIG_SETTING_ID_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> ConfigSettingID:
        return cls(_CONFIG_SETTING_ID_REVERSE_MAP[json_value])
