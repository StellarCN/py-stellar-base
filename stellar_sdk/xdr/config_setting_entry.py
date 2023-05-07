# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib3 import Packer, Unpacker

from .config_setting_id import ConfigSettingID
from .uint32 import Uint32

__all__ = ["ConfigSettingEntry"]


class ConfigSettingEntry:
    """
    XDR Source Code::

        union ConfigSettingEntry switch (ConfigSettingID configSettingID)
        {
        case CONFIG_SETTING_CONTRACT_MAX_SIZE_BYTES:
            uint32 contractMaxSizeBytes;
        };
    """

    def __init__(
        self,
        config_setting_id: ConfigSettingID,
        contract_max_size_bytes: Uint32 = None,
    ) -> None:
        self.config_setting_id = config_setting_id
        self.contract_max_size_bytes = contract_max_size_bytes

    @classmethod
    def from_config_setting_contract_max_size_bytes(
        cls, contract_max_size_bytes: Uint32
    ) -> "ConfigSettingEntry":
        return cls(
            ConfigSettingID.CONFIG_SETTING_CONTRACT_MAX_SIZE_BYTES,
            contract_max_size_bytes=contract_max_size_bytes,
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

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ConfigSettingEntry":
        config_setting_id = ConfigSettingID.unpack(unpacker)
        if config_setting_id == ConfigSettingID.CONFIG_SETTING_CONTRACT_MAX_SIZE_BYTES:
            contract_max_size_bytes = Uint32.unpack(unpacker)
            return cls(
                config_setting_id=config_setting_id,
                contract_max_size_bytes=contract_max_size_bytes,
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
        )

    def __str__(self):
        out = []
        out.append(f"config_setting_id={self.config_setting_id}")
        out.append(
            f"contract_max_size_bytes={self.contract_max_size_bytes}"
        ) if self.contract_max_size_bytes is not None else None
        return f"<ConfigSettingEntry [{', '.join(out)}]>"
