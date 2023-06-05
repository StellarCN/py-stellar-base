# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib3 import Packer, Unpacker

from .config_setting_contract_bandwidth_v0 import ConfigSettingContractBandwidthV0
from .config_setting_contract_compute_v0 import ConfigSettingContractComputeV0
from .config_setting_contract_historical_data_v0 import (
    ConfigSettingContractHistoricalDataV0,
)
from .config_setting_contract_ledger_cost_v0 import ConfigSettingContractLedgerCostV0
from .config_setting_contract_meta_data_v0 import ConfigSettingContractMetaDataV0
from .config_setting_id import ConfigSettingID
from .contract_cost_params import ContractCostParams
from .uint32 import Uint32

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
        case CONFIG_SETTING_CONTRACT_META_DATA_V0:
            ConfigSettingContractMetaDataV0 contractMetaData;
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
        };
    """

    def __init__(
        self,
        config_setting_id: ConfigSettingID,
        contract_max_size_bytes: Uint32 = None,
        contract_compute: ConfigSettingContractComputeV0 = None,
        contract_ledger_cost: ConfigSettingContractLedgerCostV0 = None,
        contract_historical_data: ConfigSettingContractHistoricalDataV0 = None,
        contract_meta_data: ConfigSettingContractMetaDataV0 = None,
        contract_bandwidth: ConfigSettingContractBandwidthV0 = None,
        contract_cost_params_cpu_insns: ContractCostParams = None,
        contract_cost_params_mem_bytes: ContractCostParams = None,
        contract_data_key_size_bytes: Uint32 = None,
        contract_data_entry_size_bytes: Uint32 = None,
    ) -> None:
        self.config_setting_id = config_setting_id
        self.contract_max_size_bytes = contract_max_size_bytes
        self.contract_compute = contract_compute
        self.contract_ledger_cost = contract_ledger_cost
        self.contract_historical_data = contract_historical_data
        self.contract_meta_data = contract_meta_data
        self.contract_bandwidth = contract_bandwidth
        self.contract_cost_params_cpu_insns = contract_cost_params_cpu_insns
        self.contract_cost_params_mem_bytes = contract_cost_params_mem_bytes
        self.contract_data_key_size_bytes = contract_data_key_size_bytes
        self.contract_data_entry_size_bytes = contract_data_entry_size_bytes

    @classmethod
    def from_config_setting_contract_max_size_bytes(
        cls, contract_max_size_bytes: Uint32
    ) -> "ConfigSettingEntry":
        return cls(
            ConfigSettingID.CONFIG_SETTING_CONTRACT_MAX_SIZE_BYTES,
            contract_max_size_bytes=contract_max_size_bytes,
        )

    @classmethod
    def from_config_setting_contract_compute_v0(
        cls, contract_compute: ConfigSettingContractComputeV0
    ) -> "ConfigSettingEntry":
        return cls(
            ConfigSettingID.CONFIG_SETTING_CONTRACT_COMPUTE_V0,
            contract_compute=contract_compute,
        )

    @classmethod
    def from_config_setting_contract_ledger_cost_v0(
        cls, contract_ledger_cost: ConfigSettingContractLedgerCostV0
    ) -> "ConfigSettingEntry":
        return cls(
            ConfigSettingID.CONFIG_SETTING_CONTRACT_LEDGER_COST_V0,
            contract_ledger_cost=contract_ledger_cost,
        )

    @classmethod
    def from_config_setting_contract_historical_data_v0(
        cls, contract_historical_data: ConfigSettingContractHistoricalDataV0
    ) -> "ConfigSettingEntry":
        return cls(
            ConfigSettingID.CONFIG_SETTING_CONTRACT_HISTORICAL_DATA_V0,
            contract_historical_data=contract_historical_data,
        )

    @classmethod
    def from_config_setting_contract_meta_data_v0(
        cls, contract_meta_data: ConfigSettingContractMetaDataV0
    ) -> "ConfigSettingEntry":
        return cls(
            ConfigSettingID.CONFIG_SETTING_CONTRACT_META_DATA_V0,
            contract_meta_data=contract_meta_data,
        )

    @classmethod
    def from_config_setting_contract_bandwidth_v0(
        cls, contract_bandwidth: ConfigSettingContractBandwidthV0
    ) -> "ConfigSettingEntry":
        return cls(
            ConfigSettingID.CONFIG_SETTING_CONTRACT_BANDWIDTH_V0,
            contract_bandwidth=contract_bandwidth,
        )

    @classmethod
    def from_config_setting_contract_cost_params_cpu_instructions(
        cls, contract_cost_params_cpu_insns: ContractCostParams
    ) -> "ConfigSettingEntry":
        return cls(
            ConfigSettingID.CONFIG_SETTING_CONTRACT_COST_PARAMS_CPU_INSTRUCTIONS,
            contract_cost_params_cpu_insns=contract_cost_params_cpu_insns,
        )

    @classmethod
    def from_config_setting_contract_cost_params_memory_bytes(
        cls, contract_cost_params_mem_bytes: ContractCostParams
    ) -> "ConfigSettingEntry":
        return cls(
            ConfigSettingID.CONFIG_SETTING_CONTRACT_COST_PARAMS_MEMORY_BYTES,
            contract_cost_params_mem_bytes=contract_cost_params_mem_bytes,
        )

    @classmethod
    def from_config_setting_contract_data_key_size_bytes(
        cls, contract_data_key_size_bytes: Uint32
    ) -> "ConfigSettingEntry":
        return cls(
            ConfigSettingID.CONFIG_SETTING_CONTRACT_DATA_KEY_SIZE_BYTES,
            contract_data_key_size_bytes=contract_data_key_size_bytes,
        )

    @classmethod
    def from_config_setting_contract_data_entry_size_bytes(
        cls, contract_data_entry_size_bytes: Uint32
    ) -> "ConfigSettingEntry":
        return cls(
            ConfigSettingID.CONFIG_SETTING_CONTRACT_DATA_ENTRY_SIZE_BYTES,
            contract_data_entry_size_bytes=contract_data_entry_size_bytes,
        )

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
        if (
            self.config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_META_DATA_V0
        ):
            if self.contract_meta_data is None:
                raise ValueError("contract_meta_data should not be None.")
            self.contract_meta_data.pack(packer)
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

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ConfigSettingEntry":
        config_setting_id = ConfigSettingID.unpack(unpacker)
        if config_setting_id == ConfigSettingID.CONFIG_SETTING_CONTRACT_MAX_SIZE_BYTES:
            contract_max_size_bytes = Uint32.unpack(unpacker)
            return cls(
                config_setting_id=config_setting_id,
                contract_max_size_bytes=contract_max_size_bytes,
            )
        if config_setting_id == ConfigSettingID.CONFIG_SETTING_CONTRACT_COMPUTE_V0:
            contract_compute = ConfigSettingContractComputeV0.unpack(unpacker)
            return cls(
                config_setting_id=config_setting_id, contract_compute=contract_compute
            )
        if config_setting_id == ConfigSettingID.CONFIG_SETTING_CONTRACT_LEDGER_COST_V0:
            contract_ledger_cost = ConfigSettingContractLedgerCostV0.unpack(unpacker)
            return cls(
                config_setting_id=config_setting_id,
                contract_ledger_cost=contract_ledger_cost,
            )
        if (
            config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_HISTORICAL_DATA_V0
        ):
            contract_historical_data = ConfigSettingContractHistoricalDataV0.unpack(
                unpacker
            )
            return cls(
                config_setting_id=config_setting_id,
                contract_historical_data=contract_historical_data,
            )
        if config_setting_id == ConfigSettingID.CONFIG_SETTING_CONTRACT_META_DATA_V0:
            contract_meta_data = ConfigSettingContractMetaDataV0.unpack(unpacker)
            return cls(
                config_setting_id=config_setting_id,
                contract_meta_data=contract_meta_data,
            )
        if config_setting_id == ConfigSettingID.CONFIG_SETTING_CONTRACT_BANDWIDTH_V0:
            contract_bandwidth = ConfigSettingContractBandwidthV0.unpack(unpacker)
            return cls(
                config_setting_id=config_setting_id,
                contract_bandwidth=contract_bandwidth,
            )
        if (
            config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_COST_PARAMS_CPU_INSTRUCTIONS
        ):
            contract_cost_params_cpu_insns = ContractCostParams.unpack(unpacker)
            return cls(
                config_setting_id=config_setting_id,
                contract_cost_params_cpu_insns=contract_cost_params_cpu_insns,
            )
        if (
            config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_COST_PARAMS_MEMORY_BYTES
        ):
            contract_cost_params_mem_bytes = ContractCostParams.unpack(unpacker)
            return cls(
                config_setting_id=config_setting_id,
                contract_cost_params_mem_bytes=contract_cost_params_mem_bytes,
            )
        if (
            config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_DATA_KEY_SIZE_BYTES
        ):
            contract_data_key_size_bytes = Uint32.unpack(unpacker)
            return cls(
                config_setting_id=config_setting_id,
                contract_data_key_size_bytes=contract_data_key_size_bytes,
            )
        if (
            config_setting_id
            == ConfigSettingID.CONFIG_SETTING_CONTRACT_DATA_ENTRY_SIZE_BYTES
        ):
            contract_data_entry_size_bytes = Uint32.unpack(unpacker)
            return cls(
                config_setting_id=config_setting_id,
                contract_data_entry_size_bytes=contract_data_entry_size_bytes,
            )
        return cls(config_setting_id=config_setting_id)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "ConfigSettingEntry":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ConfigSettingEntry":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.config_setting_id == other.config_setting_id
            and self.contract_max_size_bytes == other.contract_max_size_bytes
            and self.contract_compute == other.contract_compute
            and self.contract_ledger_cost == other.contract_ledger_cost
            and self.contract_historical_data == other.contract_historical_data
            and self.contract_meta_data == other.contract_meta_data
            and self.contract_bandwidth == other.contract_bandwidth
            and self.contract_cost_params_cpu_insns
            == other.contract_cost_params_cpu_insns
            and self.contract_cost_params_mem_bytes
            == other.contract_cost_params_mem_bytes
            and self.contract_data_key_size_bytes == other.contract_data_key_size_bytes
            and self.contract_data_entry_size_bytes
            == other.contract_data_entry_size_bytes
        )

    def __str__(self):
        out = []
        out.append(f"config_setting_id={self.config_setting_id}")
        out.append(
            f"contract_max_size_bytes={self.contract_max_size_bytes}"
        ) if self.contract_max_size_bytes is not None else None
        out.append(
            f"contract_compute={self.contract_compute}"
        ) if self.contract_compute is not None else None
        out.append(
            f"contract_ledger_cost={self.contract_ledger_cost}"
        ) if self.contract_ledger_cost is not None else None
        out.append(
            f"contract_historical_data={self.contract_historical_data}"
        ) if self.contract_historical_data is not None else None
        out.append(
            f"contract_meta_data={self.contract_meta_data}"
        ) if self.contract_meta_data is not None else None
        out.append(
            f"contract_bandwidth={self.contract_bandwidth}"
        ) if self.contract_bandwidth is not None else None
        out.append(
            f"contract_cost_params_cpu_insns={self.contract_cost_params_cpu_insns}"
        ) if self.contract_cost_params_cpu_insns is not None else None
        out.append(
            f"contract_cost_params_mem_bytes={self.contract_cost_params_mem_bytes}"
        ) if self.contract_cost_params_mem_bytes is not None else None
        out.append(
            f"contract_data_key_size_bytes={self.contract_data_key_size_bytes}"
        ) if self.contract_data_key_size_bytes is not None else None
        out.append(
            f"contract_data_entry_size_bytes={self.contract_data_entry_size_bytes}"
        ) if self.contract_data_entry_size_bytes is not None else None
        return f"<ConfigSettingEntry [{', '.join(out)}]>"
