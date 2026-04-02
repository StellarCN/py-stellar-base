# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List, Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .config_setting_contract_bandwidth_v0 import ConfigSettingContractBandwidthV0
from .config_setting_contract_compute_v0 import ConfigSettingContractComputeV0
from .config_setting_contract_events_v0 import ConfigSettingContractEventsV0
from .config_setting_contract_execution_lanes_v0 import (
    ConfigSettingContractExecutionLanesV0,
)
from .config_setting_contract_historical_data_v0 import (
    ConfigSettingContractHistoricalDataV0,
)
from .config_setting_contract_ledger_cost_ext_v0 import (
    ConfigSettingContractLedgerCostExtV0,
)
from .config_setting_contract_ledger_cost_v0 import ConfigSettingContractLedgerCostV0
from .config_setting_contract_parallel_compute_v0 import (
    ConfigSettingContractParallelComputeV0,
)
from .config_setting_id import ConfigSettingID
from .config_setting_scp_timing import ConfigSettingSCPTiming
from .contract_cost_params import ContractCostParams
from .eviction_iterator import EvictionIterator
from .freeze_bypass_txs import FreezeBypassTxs
from .freeze_bypass_txs_delta import FreezeBypassTxsDelta
from .frozen_ledger_keys import FrozenLedgerKeys
from .frozen_ledger_keys_delta import FrozenLedgerKeysDelta
from .state_archival_settings import StateArchivalSettings
from .uint32 import Uint32
from .uint64 import Uint64

__all__ = ["ConfigSettingEntry"]


class ConfigSettingEntry:
    """
    XDR Source Code::

        union ConfigSettingEntry switch (ConfigSettingID configSettingID)
        {
        case CONFIG_SETTING_CONTRACT_MAX_SIZE_BYTES:
            uint32 contractMaxSizeBytes;
        case CONFIG_SETTING_CONTRACT_COMPUTE_V0:
            ConfigSettingContractComputeV0 contractCompute;
        case CONFIG_SETTING_CONTRACT_LEDGER_COST_V0:
            ConfigSettingContractLedgerCostV0 contractLedgerCost;
        case CONFIG_SETTING_CONTRACT_HISTORICAL_DATA_V0:
            ConfigSettingContractHistoricalDataV0 contractHistoricalData;
        case CONFIG_SETTING_CONTRACT_EVENTS_V0:
            ConfigSettingContractEventsV0 contractEvents;
        case CONFIG_SETTING_CONTRACT_BANDWIDTH_V0:
            ConfigSettingContractBandwidthV0 contractBandwidth;
        case CONFIG_SETTING_CONTRACT_COST_PARAMS_CPU_INSTRUCTIONS:
            ContractCostParams contractCostParamsCpuInsns;
        case CONFIG_SETTING_CONTRACT_COST_PARAMS_MEMORY_BYTES:
            ContractCostParams contractCostParamsMemBytes;
        case CONFIG_SETTING_CONTRACT_DATA_KEY_SIZE_BYTES:
            uint32 contractDataKeySizeBytes;
        case CONFIG_SETTING_CONTRACT_DATA_ENTRY_SIZE_BYTES:
            uint32 contractDataEntrySizeBytes;
        case CONFIG_SETTING_STATE_ARCHIVAL:
            StateArchivalSettings stateArchivalSettings;
        case CONFIG_SETTING_CONTRACT_EXECUTION_LANES:
            ConfigSettingContractExecutionLanesV0 contractExecutionLanes;
        case CONFIG_SETTING_LIVE_SOROBAN_STATE_SIZE_WINDOW:
            uint64 liveSorobanStateSizeWindow<>;
        case CONFIG_SETTING_EVICTION_ITERATOR:
            EvictionIterator evictionIterator;
        case CONFIG_SETTING_CONTRACT_PARALLEL_COMPUTE_V0:
            ConfigSettingContractParallelComputeV0 contractParallelCompute;
        case CONFIG_SETTING_CONTRACT_LEDGER_COST_EXT_V0:
            ConfigSettingContractLedgerCostExtV0 contractLedgerCostExt;
        case CONFIG_SETTING_SCP_TIMING:
            ConfigSettingSCPTiming contractSCPTiming;
        case CONFIG_SETTING_FROZEN_LEDGER_KEYS:
            FrozenLedgerKeys frozenLedgerKeys;
        case CONFIG_SETTING_FROZEN_LEDGER_KEYS_DELTA:
            FrozenLedgerKeysDelta frozenLedgerKeysDelta;
        case CONFIG_SETTING_FREEZE_BYPASS_TXS:
            FreezeBypassTxs freezeBypassTxs;
        case CONFIG_SETTING_FREEZE_BYPASS_TXS_DELTA:
            FreezeBypassTxsDelta freezeBypassTxsDelta;
        };
    """

    def __init__(
        self,
        config_setting_id: ConfigSettingID,
        contract_max_size_bytes: Optional[Uint32] = None,
        contract_compute: Optional[ConfigSettingContractComputeV0] = None,
        contract_ledger_cost: Optional[ConfigSettingContractLedgerCostV0] = None,
        contract_historical_data: Optional[
            ConfigSettingContractHistoricalDataV0
        ] = None,
        contract_events: Optional[ConfigSettingContractEventsV0] = None,
        contract_bandwidth: Optional[ConfigSettingContractBandwidthV0] = None,
        contract_cost_params_cpu_insns: Optional[ContractCostParams] = None,
        contract_cost_params_mem_bytes: Optional[ContractCostParams] = None,
        contract_data_key_size_bytes: Optional[Uint32] = None,
        contract_data_entry_size_bytes: Optional[Uint32] = None,
        state_archival_settings: Optional[StateArchivalSettings] = None,
        contract_execution_lanes: Optional[
            ConfigSettingContractExecutionLanesV0
        ] = None,
        live_soroban_state_size_window: Optional[List[Uint64]] = None,
        eviction_iterator: Optional[EvictionIterator] = None,
        contract_parallel_compute: Optional[
            ConfigSettingContractParallelComputeV0
        ] = None,
        contract_ledger_cost_ext: Optional[ConfigSettingContractLedgerCostExtV0] = None,
        contract_scp_timing: Optional[ConfigSettingSCPTiming] = None,
        frozen_ledger_keys: Optional[FrozenLedgerKeys] = None,
        frozen_ledger_keys_delta: Optional[FrozenLedgerKeysDelta] = None,
        freeze_bypass_txs: Optional[FreezeBypassTxs] = None,
        freeze_bypass_txs_delta: Optional[FreezeBypassTxsDelta] = None,
    ) -> None:
        _expect_max_length = 4294967295
        if (
            live_soroban_state_size_window
            and len(live_soroban_state_size_window) > _expect_max_length
        ):
            raise ValueError(
                f"The maximum length of `live_soroban_state_size_window` should be {_expect_max_length}, but got {len(live_soroban_state_size_window)}."
            )
        self.config_setting_id = config_setting_id
        self.contract_max_size_bytes = contract_max_size_bytes
        self.contract_compute = contract_compute
        self.contract_ledger_cost = contract_ledger_cost
        self.contract_historical_data = contract_historical_data
        self.contract_events = contract_events
        self.contract_bandwidth = contract_bandwidth
        self.contract_cost_params_cpu_insns = contract_cost_params_cpu_insns
        self.contract_cost_params_mem_bytes = contract_cost_params_mem_bytes
        self.contract_data_key_size_bytes = contract_data_key_size_bytes
        self.contract_data_entry_size_bytes = contract_data_entry_size_bytes
        self.state_archival_settings = state_archival_settings
        self.contract_execution_lanes = contract_execution_lanes
        self.live_soroban_state_size_window = live_soroban_state_size_window
        self.eviction_iterator = eviction_iterator
        self.contract_parallel_compute = contract_parallel_compute
        self.contract_ledger_cost_ext = contract_ledger_cost_ext
        self.contract_scp_timing = contract_scp_timing
        self.frozen_ledger_keys = frozen_ledger_keys
        self.frozen_ledger_keys_delta = frozen_ledger_keys_delta
        self.freeze_bypass_txs = freeze_bypass_txs
        self.freeze_bypass_txs_delta = freeze_bypass_txs_delta

    def pack(self, packer: Packer) -> None:
        self.config_setting_id.pack(packer)
        if (
            self.config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_MAX_SIZE_BYTES
        ):
            if self.contract_max_size_bytes is None:
                raise ValueError("contract_max_size_bytes should not be None.")
            self.contract_max_size_bytes.pack(packer)
            return
        if self.config_setting_id == ConfigSettingID.CONFIG_SETTING_CONTRACT_COMPUTE_V0:
            if self.contract_compute is None:
                raise ValueError("contract_compute should not be None.")
            self.contract_compute.pack(packer)
            return
        if (
            self.config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_LEDGER_COST_V0
        ):
            if self.contract_ledger_cost is None:
                raise ValueError("contract_ledger_cost should not be None.")
            self.contract_ledger_cost.pack(packer)
            return
        if (
            self.config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_HISTORICAL_DATA_V0
        ):
            if self.contract_historical_data is None:
                raise ValueError("contract_historical_data should not be None.")
            self.contract_historical_data.pack(packer)
            return
        if self.config_setting_id == ConfigSettingID.CONFIG_SETTING_CONTRACT_EVENTS_V0:
            if self.contract_events is None:
                raise ValueError("contract_events should not be None.")
            self.contract_events.pack(packer)
            return
        if (
            self.config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_BANDWIDTH_V0
        ):
            if self.contract_bandwidth is None:
                raise ValueError("contract_bandwidth should not be None.")
            self.contract_bandwidth.pack(packer)
            return
        if (
            self.config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_COST_PARAMS_CPU_INSTRUCTIONS
        ):
            if self.contract_cost_params_cpu_insns is None:
                raise ValueError("contract_cost_params_cpu_insns should not be None.")
            self.contract_cost_params_cpu_insns.pack(packer)
            return
        if (
            self.config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_COST_PARAMS_MEMORY_BYTES
        ):
            if self.contract_cost_params_mem_bytes is None:
                raise ValueError("contract_cost_params_mem_bytes should not be None.")
            self.contract_cost_params_mem_bytes.pack(packer)
            return
        if (
            self.config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_DATA_KEY_SIZE_BYTES
        ):
            if self.contract_data_key_size_bytes is None:
                raise ValueError("contract_data_key_size_bytes should not be None.")
            self.contract_data_key_size_bytes.pack(packer)
            return
        if (
            self.config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_DATA_ENTRY_SIZE_BYTES
        ):
            if self.contract_data_entry_size_bytes is None:
                raise ValueError("contract_data_entry_size_bytes should not be None.")
            self.contract_data_entry_size_bytes.pack(packer)
            return
        if self.config_setting_id == ConfigSettingID.CONFIG_SETTING_STATE_ARCHIVAL:
            if self.state_archival_settings is None:
                raise ValueError("state_archival_settings should not be None.")
            self.state_archival_settings.pack(packer)
            return
        if (
            self.config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_EXECUTION_LANES
        ):
            if self.contract_execution_lanes is None:
                raise ValueError("contract_execution_lanes should not be None.")
            self.contract_execution_lanes.pack(packer)
            return
        if (
            self.config_setting_id
            == ConfigSettingID.CONFIG_SETTING_LIVE_SOROBAN_STATE_SIZE_WINDOW
        ):
            if self.live_soroban_state_size_window is None:
                raise ValueError("live_soroban_state_size_window should not be None.")
            packer.pack_uint(len(self.live_soroban_state_size_window))
            for (
                live_soroban_state_size_window_item
            ) in self.live_soroban_state_size_window:
                live_soroban_state_size_window_item.pack(packer)
            return
        if self.config_setting_id == ConfigSettingID.CONFIG_SETTING_EVICTION_ITERATOR:
            if self.eviction_iterator is None:
                raise ValueError("eviction_iterator should not be None.")
            self.eviction_iterator.pack(packer)
            return
        if (
            self.config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_PARALLEL_COMPUTE_V0
        ):
            if self.contract_parallel_compute is None:
                raise ValueError("contract_parallel_compute should not be None.")
            self.contract_parallel_compute.pack(packer)
            return
        if (
            self.config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_LEDGER_COST_EXT_V0
        ):
            if self.contract_ledger_cost_ext is None:
                raise ValueError("contract_ledger_cost_ext should not be None.")
            self.contract_ledger_cost_ext.pack(packer)
            return
        if self.config_setting_id == ConfigSettingID.CONFIG_SETTING_SCP_TIMING:
            if self.contract_scp_timing is None:
                raise ValueError("contract_scp_timing should not be None.")
            self.contract_scp_timing.pack(packer)
            return
        if self.config_setting_id == ConfigSettingID.CONFIG_SETTING_FROZEN_LEDGER_KEYS:
            if self.frozen_ledger_keys is None:
                raise ValueError("frozen_ledger_keys should not be None.")
            self.frozen_ledger_keys.pack(packer)
            return
        if (
            self.config_setting_id
            == ConfigSettingID.CONFIG_SETTING_FROZEN_LEDGER_KEYS_DELTA
        ):
            if self.frozen_ledger_keys_delta is None:
                raise ValueError("frozen_ledger_keys_delta should not be None.")
            self.frozen_ledger_keys_delta.pack(packer)
            return
        if self.config_setting_id == ConfigSettingID.CONFIG_SETTING_FREEZE_BYPASS_TXS:
            if self.freeze_bypass_txs is None:
                raise ValueError("freeze_bypass_txs should not be None.")
            self.freeze_bypass_txs.pack(packer)
            return
        if (
            self.config_setting_id
            == ConfigSettingID.CONFIG_SETTING_FREEZE_BYPASS_TXS_DELTA
        ):
            if self.freeze_bypass_txs_delta is None:
                raise ValueError("freeze_bypass_txs_delta should not be None.")
            self.freeze_bypass_txs_delta.pack(packer)
            return
        raise ValueError("Invalid config_setting_id.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ConfigSettingEntry:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        config_setting_id = ConfigSettingID.unpack(unpacker)
        if config_setting_id == ConfigSettingID.CONFIG_SETTING_CONTRACT_MAX_SIZE_BYTES:
            contract_max_size_bytes = Uint32.unpack(unpacker, depth_limit - 1)
            return cls(
                config_setting_id=config_setting_id,
                contract_max_size_bytes=contract_max_size_bytes,
            )
        if config_setting_id == ConfigSettingID.CONFIG_SETTING_CONTRACT_COMPUTE_V0:
            contract_compute = ConfigSettingContractComputeV0.unpack(
                unpacker, depth_limit - 1
            )
            return cls(
                config_setting_id=config_setting_id, contract_compute=contract_compute
            )
        if config_setting_id == ConfigSettingID.CONFIG_SETTING_CONTRACT_LEDGER_COST_V0:
            contract_ledger_cost = ConfigSettingContractLedgerCostV0.unpack(
                unpacker, depth_limit - 1
            )
            return cls(
                config_setting_id=config_setting_id,
                contract_ledger_cost=contract_ledger_cost,
            )
        if (
            config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_HISTORICAL_DATA_V0
        ):
            contract_historical_data = ConfigSettingContractHistoricalDataV0.unpack(
                unpacker, depth_limit - 1
            )
            return cls(
                config_setting_id=config_setting_id,
                contract_historical_data=contract_historical_data,
            )
        if config_setting_id == ConfigSettingID.CONFIG_SETTING_CONTRACT_EVENTS_V0:
            contract_events = ConfigSettingContractEventsV0.unpack(
                unpacker, depth_limit - 1
            )
            return cls(
                config_setting_id=config_setting_id, contract_events=contract_events
            )
        if config_setting_id == ConfigSettingID.CONFIG_SETTING_CONTRACT_BANDWIDTH_V0:
            contract_bandwidth = ConfigSettingContractBandwidthV0.unpack(
                unpacker, depth_limit - 1
            )
            return cls(
                config_setting_id=config_setting_id,
                contract_bandwidth=contract_bandwidth,
            )
        if (
            config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_COST_PARAMS_CPU_INSTRUCTIONS
        ):
            contract_cost_params_cpu_insns = ContractCostParams.unpack(
                unpacker, depth_limit - 1
            )
            return cls(
                config_setting_id=config_setting_id,
                contract_cost_params_cpu_insns=contract_cost_params_cpu_insns,
            )
        if (
            config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_COST_PARAMS_MEMORY_BYTES
        ):
            contract_cost_params_mem_bytes = ContractCostParams.unpack(
                unpacker, depth_limit - 1
            )
            return cls(
                config_setting_id=config_setting_id,
                contract_cost_params_mem_bytes=contract_cost_params_mem_bytes,
            )
        if (
            config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_DATA_KEY_SIZE_BYTES
        ):
            contract_data_key_size_bytes = Uint32.unpack(unpacker, depth_limit - 1)
            return cls(
                config_setting_id=config_setting_id,
                contract_data_key_size_bytes=contract_data_key_size_bytes,
            )
        if (
            config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_DATA_ENTRY_SIZE_BYTES
        ):
            contract_data_entry_size_bytes = Uint32.unpack(unpacker, depth_limit - 1)
            return cls(
                config_setting_id=config_setting_id,
                contract_data_entry_size_bytes=contract_data_entry_size_bytes,
            )
        if config_setting_id == ConfigSettingID.CONFIG_SETTING_STATE_ARCHIVAL:
            state_archival_settings = StateArchivalSettings.unpack(
                unpacker, depth_limit - 1
            )
            return cls(
                config_setting_id=config_setting_id,
                state_archival_settings=state_archival_settings,
            )
        if config_setting_id == ConfigSettingID.CONFIG_SETTING_CONTRACT_EXECUTION_LANES:
            contract_execution_lanes = ConfigSettingContractExecutionLanesV0.unpack(
                unpacker, depth_limit - 1
            )
            return cls(
                config_setting_id=config_setting_id,
                contract_execution_lanes=contract_execution_lanes,
            )
        if (
            config_setting_id
            == ConfigSettingID.CONFIG_SETTING_LIVE_SOROBAN_STATE_SIZE_WINDOW
        ):
            length = unpacker.unpack_uint()
            _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
            if _remaining < length:
                raise ValueError(
                    f"live_soroban_state_size_window length {length} exceeds remaining input length {_remaining}"
                )
            live_soroban_state_size_window = []
            for _ in range(length):
                live_soroban_state_size_window.append(
                    Uint64.unpack(unpacker, depth_limit - 1)
                )
            return cls(
                config_setting_id=config_setting_id,
                live_soroban_state_size_window=live_soroban_state_size_window,
            )
        if config_setting_id == ConfigSettingID.CONFIG_SETTING_EVICTION_ITERATOR:
            eviction_iterator = EvictionIterator.unpack(unpacker, depth_limit - 1)
            return cls(
                config_setting_id=config_setting_id, eviction_iterator=eviction_iterator
            )
        if (
            config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_PARALLEL_COMPUTE_V0
        ):
            contract_parallel_compute = ConfigSettingContractParallelComputeV0.unpack(
                unpacker, depth_limit - 1
            )
            return cls(
                config_setting_id=config_setting_id,
                contract_parallel_compute=contract_parallel_compute,
            )
        if (
            config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_LEDGER_COST_EXT_V0
        ):
            contract_ledger_cost_ext = ConfigSettingContractLedgerCostExtV0.unpack(
                unpacker, depth_limit - 1
            )
            return cls(
                config_setting_id=config_setting_id,
                contract_ledger_cost_ext=contract_ledger_cost_ext,
            )
        if config_setting_id == ConfigSettingID.CONFIG_SETTING_SCP_TIMING:
            contract_scp_timing = ConfigSettingSCPTiming.unpack(
                unpacker, depth_limit - 1
            )
            return cls(
                config_setting_id=config_setting_id,
                contract_scp_timing=contract_scp_timing,
            )
        if config_setting_id == ConfigSettingID.CONFIG_SETTING_FROZEN_LEDGER_KEYS:
            frozen_ledger_keys = FrozenLedgerKeys.unpack(unpacker, depth_limit - 1)
            return cls(
                config_setting_id=config_setting_id,
                frozen_ledger_keys=frozen_ledger_keys,
            )
        if config_setting_id == ConfigSettingID.CONFIG_SETTING_FROZEN_LEDGER_KEYS_DELTA:
            frozen_ledger_keys_delta = FrozenLedgerKeysDelta.unpack(
                unpacker, depth_limit - 1
            )
            return cls(
                config_setting_id=config_setting_id,
                frozen_ledger_keys_delta=frozen_ledger_keys_delta,
            )
        if config_setting_id == ConfigSettingID.CONFIG_SETTING_FREEZE_BYPASS_TXS:
            freeze_bypass_txs = FreezeBypassTxs.unpack(unpacker, depth_limit - 1)
            return cls(
                config_setting_id=config_setting_id, freeze_bypass_txs=freeze_bypass_txs
            )
        if config_setting_id == ConfigSettingID.CONFIG_SETTING_FREEZE_BYPASS_TXS_DELTA:
            freeze_bypass_txs_delta = FreezeBypassTxsDelta.unpack(
                unpacker, depth_limit - 1
            )
            return cls(
                config_setting_id=config_setting_id,
                freeze_bypass_txs_delta=freeze_bypass_txs_delta,
            )
        raise ValueError("Invalid config_setting_id.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ConfigSettingEntry:
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
    def from_xdr(cls, xdr: str) -> ConfigSettingEntry:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ConfigSettingEntry:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if (
            self.config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_MAX_SIZE_BYTES
        ):
            assert self.contract_max_size_bytes is not None
            return {
                "contract_max_size_bytes": self.contract_max_size_bytes.to_json_dict()
            }
        if self.config_setting_id == ConfigSettingID.CONFIG_SETTING_CONTRACT_COMPUTE_V0:
            assert self.contract_compute is not None
            return {"contract_compute_v0": self.contract_compute.to_json_dict()}
        if (
            self.config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_LEDGER_COST_V0
        ):
            assert self.contract_ledger_cost is not None
            return {"contract_ledger_cost_v0": self.contract_ledger_cost.to_json_dict()}
        if (
            self.config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_HISTORICAL_DATA_V0
        ):
            assert self.contract_historical_data is not None
            return {
                "contract_historical_data_v0": self.contract_historical_data.to_json_dict()
            }
        if self.config_setting_id == ConfigSettingID.CONFIG_SETTING_CONTRACT_EVENTS_V0:
            assert self.contract_events is not None
            return {"contract_events_v0": self.contract_events.to_json_dict()}
        if (
            self.config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_BANDWIDTH_V0
        ):
            assert self.contract_bandwidth is not None
            return {"contract_bandwidth_v0": self.contract_bandwidth.to_json_dict()}
        if (
            self.config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_COST_PARAMS_CPU_INSTRUCTIONS
        ):
            assert self.contract_cost_params_cpu_insns is not None
            return {
                "contract_cost_params_cpu_instructions": self.contract_cost_params_cpu_insns.to_json_dict()
            }
        if (
            self.config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_COST_PARAMS_MEMORY_BYTES
        ):
            assert self.contract_cost_params_mem_bytes is not None
            return {
                "contract_cost_params_memory_bytes": self.contract_cost_params_mem_bytes.to_json_dict()
            }
        if (
            self.config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_DATA_KEY_SIZE_BYTES
        ):
            assert self.contract_data_key_size_bytes is not None
            return {
                "contract_data_key_size_bytes": self.contract_data_key_size_bytes.to_json_dict()
            }
        if (
            self.config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_DATA_ENTRY_SIZE_BYTES
        ):
            assert self.contract_data_entry_size_bytes is not None
            return {
                "contract_data_entry_size_bytes": self.contract_data_entry_size_bytes.to_json_dict()
            }
        if self.config_setting_id == ConfigSettingID.CONFIG_SETTING_STATE_ARCHIVAL:
            assert self.state_archival_settings is not None
            return {"state_archival": self.state_archival_settings.to_json_dict()}
        if (
            self.config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_EXECUTION_LANES
        ):
            assert self.contract_execution_lanes is not None
            return {
                "contract_execution_lanes": self.contract_execution_lanes.to_json_dict()
            }
        if (
            self.config_setting_id
            == ConfigSettingID.CONFIG_SETTING_LIVE_SOROBAN_STATE_SIZE_WINDOW
        ):
            assert self.live_soroban_state_size_window is not None
            return {
                "live_soroban_state_size_window": [
                    item.to_json_dict() for item in self.live_soroban_state_size_window
                ]
            }
        if self.config_setting_id == ConfigSettingID.CONFIG_SETTING_EVICTION_ITERATOR:
            assert self.eviction_iterator is not None
            return {"eviction_iterator": self.eviction_iterator.to_json_dict()}
        if (
            self.config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_PARALLEL_COMPUTE_V0
        ):
            assert self.contract_parallel_compute is not None
            return {
                "contract_parallel_compute_v0": self.contract_parallel_compute.to_json_dict()
            }
        if (
            self.config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_LEDGER_COST_EXT_V0
        ):
            assert self.contract_ledger_cost_ext is not None
            return {
                "contract_ledger_cost_ext_v0": self.contract_ledger_cost_ext.to_json_dict()
            }
        if self.config_setting_id == ConfigSettingID.CONFIG_SETTING_SCP_TIMING:
            assert self.contract_scp_timing is not None
            return {"scp_timing": self.contract_scp_timing.to_json_dict()}
        if self.config_setting_id == ConfigSettingID.CONFIG_SETTING_FROZEN_LEDGER_KEYS:
            assert self.frozen_ledger_keys is not None
            return {"frozen_ledger_keys": self.frozen_ledger_keys.to_json_dict()}
        if (
            self.config_setting_id
            == ConfigSettingID.CONFIG_SETTING_FROZEN_LEDGER_KEYS_DELTA
        ):
            assert self.frozen_ledger_keys_delta is not None
            return {
                "frozen_ledger_keys_delta": self.frozen_ledger_keys_delta.to_json_dict()
            }
        if self.config_setting_id == ConfigSettingID.CONFIG_SETTING_FREEZE_BYPASS_TXS:
            assert self.freeze_bypass_txs is not None
            return {"freeze_bypass_txs": self.freeze_bypass_txs.to_json_dict()}
        if (
            self.config_setting_id
            == ConfigSettingID.CONFIG_SETTING_FREEZE_BYPASS_TXS_DELTA
        ):
            assert self.freeze_bypass_txs_delta is not None
            return {
                "freeze_bypass_txs_delta": self.freeze_bypass_txs_delta.to_json_dict()
            }
        raise ValueError(
            f"Unknown config_setting_id in ConfigSettingEntry: {self.config_setting_id}"
        )

    @classmethod
    def from_json_dict(cls, json_value: dict) -> ConfigSettingEntry:
        if len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for ConfigSettingEntry, got: {json_value}"
            )
        key = next(iter(json_value))
        config_setting_id = ConfigSettingID.from_json_dict(key)
        if key == "contract_max_size_bytes":
            contract_max_size_bytes = Uint32.from_json_dict(
                json_value["contract_max_size_bytes"]
            )
            return cls(
                config_setting_id=config_setting_id,
                contract_max_size_bytes=contract_max_size_bytes,
            )
        if key == "contract_compute_v0":
            contract_compute = ConfigSettingContractComputeV0.from_json_dict(
                json_value["contract_compute_v0"]
            )
            return cls(
                config_setting_id=config_setting_id, contract_compute=contract_compute
            )
        if key == "contract_ledger_cost_v0":
            contract_ledger_cost = ConfigSettingContractLedgerCostV0.from_json_dict(
                json_value["contract_ledger_cost_v0"]
            )
            return cls(
                config_setting_id=config_setting_id,
                contract_ledger_cost=contract_ledger_cost,
            )
        if key == "contract_historical_data_v0":
            contract_historical_data = (
                ConfigSettingContractHistoricalDataV0.from_json_dict(
                    json_value["contract_historical_data_v0"]
                )
            )
            return cls(
                config_setting_id=config_setting_id,
                contract_historical_data=contract_historical_data,
            )
        if key == "contract_events_v0":
            contract_events = ConfigSettingContractEventsV0.from_json_dict(
                json_value["contract_events_v0"]
            )
            return cls(
                config_setting_id=config_setting_id, contract_events=contract_events
            )
        if key == "contract_bandwidth_v0":
            contract_bandwidth = ConfigSettingContractBandwidthV0.from_json_dict(
                json_value["contract_bandwidth_v0"]
            )
            return cls(
                config_setting_id=config_setting_id,
                contract_bandwidth=contract_bandwidth,
            )
        if key == "contract_cost_params_cpu_instructions":
            contract_cost_params_cpu_insns = ContractCostParams.from_json_dict(
                json_value["contract_cost_params_cpu_instructions"]
            )
            return cls(
                config_setting_id=config_setting_id,
                contract_cost_params_cpu_insns=contract_cost_params_cpu_insns,
            )
        if key == "contract_cost_params_memory_bytes":
            contract_cost_params_mem_bytes = ContractCostParams.from_json_dict(
                json_value["contract_cost_params_memory_bytes"]
            )
            return cls(
                config_setting_id=config_setting_id,
                contract_cost_params_mem_bytes=contract_cost_params_mem_bytes,
            )
        if key == "contract_data_key_size_bytes":
            contract_data_key_size_bytes = Uint32.from_json_dict(
                json_value["contract_data_key_size_bytes"]
            )
            return cls(
                config_setting_id=config_setting_id,
                contract_data_key_size_bytes=contract_data_key_size_bytes,
            )
        if key == "contract_data_entry_size_bytes":
            contract_data_entry_size_bytes = Uint32.from_json_dict(
                json_value["contract_data_entry_size_bytes"]
            )
            return cls(
                config_setting_id=config_setting_id,
                contract_data_entry_size_bytes=contract_data_entry_size_bytes,
            )
        if key == "state_archival":
            state_archival_settings = StateArchivalSettings.from_json_dict(
                json_value["state_archival"]
            )
            return cls(
                config_setting_id=config_setting_id,
                state_archival_settings=state_archival_settings,
            )
        if key == "contract_execution_lanes":
            contract_execution_lanes = (
                ConfigSettingContractExecutionLanesV0.from_json_dict(
                    json_value["contract_execution_lanes"]
                )
            )
            return cls(
                config_setting_id=config_setting_id,
                contract_execution_lanes=contract_execution_lanes,
            )
        if key == "live_soroban_state_size_window":
            live_soroban_state_size_window = [
                Uint64.from_json_dict(item)
                for item in json_value["live_soroban_state_size_window"]
            ]
            return cls(
                config_setting_id=config_setting_id,
                live_soroban_state_size_window=live_soroban_state_size_window,
            )
        if key == "eviction_iterator":
            eviction_iterator = EvictionIterator.from_json_dict(
                json_value["eviction_iterator"]
            )
            return cls(
                config_setting_id=config_setting_id, eviction_iterator=eviction_iterator
            )
        if key == "contract_parallel_compute_v0":
            contract_parallel_compute = (
                ConfigSettingContractParallelComputeV0.from_json_dict(
                    json_value["contract_parallel_compute_v0"]
                )
            )
            return cls(
                config_setting_id=config_setting_id,
                contract_parallel_compute=contract_parallel_compute,
            )
        if key == "contract_ledger_cost_ext_v0":
            contract_ledger_cost_ext = (
                ConfigSettingContractLedgerCostExtV0.from_json_dict(
                    json_value["contract_ledger_cost_ext_v0"]
                )
            )
            return cls(
                config_setting_id=config_setting_id,
                contract_ledger_cost_ext=contract_ledger_cost_ext,
            )
        if key == "scp_timing":
            contract_scp_timing = ConfigSettingSCPTiming.from_json_dict(
                json_value["scp_timing"]
            )
            return cls(
                config_setting_id=config_setting_id,
                contract_scp_timing=contract_scp_timing,
            )
        if key == "frozen_ledger_keys":
            frozen_ledger_keys = FrozenLedgerKeys.from_json_dict(
                json_value["frozen_ledger_keys"]
            )
            return cls(
                config_setting_id=config_setting_id,
                frozen_ledger_keys=frozen_ledger_keys,
            )
        if key == "frozen_ledger_keys_delta":
            frozen_ledger_keys_delta = FrozenLedgerKeysDelta.from_json_dict(
                json_value["frozen_ledger_keys_delta"]
            )
            return cls(
                config_setting_id=config_setting_id,
                frozen_ledger_keys_delta=frozen_ledger_keys_delta,
            )
        if key == "freeze_bypass_txs":
            freeze_bypass_txs = FreezeBypassTxs.from_json_dict(
                json_value["freeze_bypass_txs"]
            )
            return cls(
                config_setting_id=config_setting_id, freeze_bypass_txs=freeze_bypass_txs
            )
        if key == "freeze_bypass_txs_delta":
            freeze_bypass_txs_delta = FreezeBypassTxsDelta.from_json_dict(
                json_value["freeze_bypass_txs_delta"]
            )
            return cls(
                config_setting_id=config_setting_id,
                freeze_bypass_txs_delta=freeze_bypass_txs_delta,
            )
        raise ValueError(f"Unknown key '{key}' for ConfigSettingEntry")

    def __hash__(self):
        return hash(
            (
                self.config_setting_id,
                self.contract_max_size_bytes,
                self.contract_compute,
                self.contract_ledger_cost,
                self.contract_historical_data,
                self.contract_events,
                self.contract_bandwidth,
                self.contract_cost_params_cpu_insns,
                self.contract_cost_params_mem_bytes,
                self.contract_data_key_size_bytes,
                self.contract_data_entry_size_bytes,
                self.state_archival_settings,
                self.contract_execution_lanes,
                self.live_soroban_state_size_window,
                self.eviction_iterator,
                self.contract_parallel_compute,
                self.contract_ledger_cost_ext,
                self.contract_scp_timing,
                self.frozen_ledger_keys,
                self.frozen_ledger_keys_delta,
                self.freeze_bypass_txs,
                self.freeze_bypass_txs_delta,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.config_setting_id == other.config_setting_id
            and self.contract_max_size_bytes == other.contract_max_size_bytes
            and self.contract_compute == other.contract_compute
            and self.contract_ledger_cost == other.contract_ledger_cost
            and self.contract_historical_data == other.contract_historical_data
            and self.contract_events == other.contract_events
            and self.contract_bandwidth == other.contract_bandwidth
            and self.contract_cost_params_cpu_insns
            == other.contract_cost_params_cpu_insns
            and self.contract_cost_params_mem_bytes
            == other.contract_cost_params_mem_bytes
            and self.contract_data_key_size_bytes == other.contract_data_key_size_bytes
            and self.contract_data_entry_size_bytes
            == other.contract_data_entry_size_bytes
            and self.state_archival_settings == other.state_archival_settings
            and self.contract_execution_lanes == other.contract_execution_lanes
            and self.live_soroban_state_size_window
            == other.live_soroban_state_size_window
            and self.eviction_iterator == other.eviction_iterator
            and self.contract_parallel_compute == other.contract_parallel_compute
            and self.contract_ledger_cost_ext == other.contract_ledger_cost_ext
            and self.contract_scp_timing == other.contract_scp_timing
            and self.frozen_ledger_keys == other.frozen_ledger_keys
            and self.frozen_ledger_keys_delta == other.frozen_ledger_keys_delta
            and self.freeze_bypass_txs == other.freeze_bypass_txs
            and self.freeze_bypass_txs_delta == other.freeze_bypass_txs_delta
        )

    def __repr__(self):
        out = []
        out.append(f"config_setting_id={self.config_setting_id}")
        if self.contract_max_size_bytes is not None:
            out.append(f"contract_max_size_bytes={self.contract_max_size_bytes}")
        if self.contract_compute is not None:
            out.append(f"contract_compute={self.contract_compute}")
        if self.contract_ledger_cost is not None:
            out.append(f"contract_ledger_cost={self.contract_ledger_cost}")
        if self.contract_historical_data is not None:
            out.append(f"contract_historical_data={self.contract_historical_data}")
        if self.contract_events is not None:
            out.append(f"contract_events={self.contract_events}")
        if self.contract_bandwidth is not None:
            out.append(f"contract_bandwidth={self.contract_bandwidth}")
        if self.contract_cost_params_cpu_insns is not None:
            out.append(
                f"contract_cost_params_cpu_insns={self.contract_cost_params_cpu_insns}"
            )
        if self.contract_cost_params_mem_bytes is not None:
            out.append(
                f"contract_cost_params_mem_bytes={self.contract_cost_params_mem_bytes}"
            )
        if self.contract_data_key_size_bytes is not None:
            out.append(
                f"contract_data_key_size_bytes={self.contract_data_key_size_bytes}"
            )
        if self.contract_data_entry_size_bytes is not None:
            out.append(
                f"contract_data_entry_size_bytes={self.contract_data_entry_size_bytes}"
            )
        if self.state_archival_settings is not None:
            out.append(f"state_archival_settings={self.state_archival_settings}")
        if self.contract_execution_lanes is not None:
            out.append(f"contract_execution_lanes={self.contract_execution_lanes}")
        if self.live_soroban_state_size_window is not None:
            out.append(
                f"live_soroban_state_size_window={self.live_soroban_state_size_window}"
            )
        if self.eviction_iterator is not None:
            out.append(f"eviction_iterator={self.eviction_iterator}")
        if self.contract_parallel_compute is not None:
            out.append(f"contract_parallel_compute={self.contract_parallel_compute}")
        if self.contract_ledger_cost_ext is not None:
            out.append(f"contract_ledger_cost_ext={self.contract_ledger_cost_ext}")
        if self.contract_scp_timing is not None:
            out.append(f"contract_scp_timing={self.contract_scp_timing}")
        if self.frozen_ledger_keys is not None:
            out.append(f"frozen_ledger_keys={self.frozen_ledger_keys}")
        if self.frozen_ledger_keys_delta is not None:
            out.append(f"frozen_ledger_keys_delta={self.frozen_ledger_keys_delta}")
        if self.freeze_bypass_txs is not None:
            out.append(f"freeze_bypass_txs={self.freeze_bypass_txs}")
        if self.freeze_bypass_txs_delta is not None:
            out.append(f"freeze_bypass_txs_delta={self.freeze_bypass_txs_delta}")
        return f"<ConfigSettingEntry [{', '.join(out)}]>"
