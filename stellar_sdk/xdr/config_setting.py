# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib3 import Packer, Unpacker

from .config_setting_type import ConfigSettingType
from .uint32 import Uint32

__all__ = ["ConfigSetting"]


class ConfigSetting:
    """
    XDR Source Code::

        union ConfigSetting switch (ConfigSettingType type)
        {
        case CONFIG_SETTING_TYPE_UINT32:
            uint32 uint32Val;
        };
    """

    def __init__(
        self,
        type: ConfigSettingType,
        uint32_val: Uint32 = None,
    ) -> None:
        self.type = type
        self.uint32_val = uint32_val

    @classmethod
    def from_config_setting_type_uint32(cls, uint32_val: Uint32) -> "ConfigSetting":
        return cls(ConfigSettingType.CONFIG_SETTING_TYPE_UINT32, uint32_val=uint32_val)

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == ConfigSettingType.CONFIG_SETTING_TYPE_UINT32:
            if self.uint32_val is None:
                raise ValueError("uint32_val should not be None.")
            self.uint32_val.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ConfigSetting":
        type = ConfigSettingType.unpack(unpacker)
        if type == ConfigSettingType.CONFIG_SETTING_TYPE_UINT32:
            uint32_val = Uint32.unpack(unpacker)
            return cls(type=type, uint32_val=uint32_val)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "ConfigSetting":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ConfigSetting":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.type == other.type and self.uint32_val == other.uint32_val

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(
            f"uint32_val={self.uint32_val}"
        ) if self.uint32_val is not None else None
        return f"<ConfigSetting [{', '.join(out)}]>"
