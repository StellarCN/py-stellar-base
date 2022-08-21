# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .config_setting import ConfigSetting
from .config_setting_entry_ext import ConfigSettingEntryExt
from .config_setting_id import ConfigSettingID

__all__ = ["ConfigSettingEntry"]


class ConfigSettingEntry:
    """
    XDR Source Code::

        struct ConfigSettingEntry
        {
            union switch (int v)
            {
            case 0:
                void;
            }
            ext;

            ConfigSettingID configSettingID;
            ConfigSetting setting;
        };
    """

    def __init__(
        self,
        ext: ConfigSettingEntryExt,
        config_setting_id: ConfigSettingID,
        setting: ConfigSetting,
    ) -> None:
        self.ext = ext
        self.config_setting_id = config_setting_id
        self.setting = setting

    def pack(self, packer: Packer) -> None:
        self.ext.pack(packer)
        self.config_setting_id.pack(packer)
        self.setting.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ConfigSettingEntry":
        ext = ConfigSettingEntryExt.unpack(unpacker)
        config_setting_id = ConfigSettingID.unpack(unpacker)
        setting = ConfigSetting.unpack(unpacker)
        return cls(
            ext=ext,
            config_setting_id=config_setting_id,
            setting=setting,
        )

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
            self.ext == other.ext
            and self.config_setting_id == other.config_setting_id
            and self.setting == other.setting
        )

    def __str__(self):
        out = [
            f"ext={self.ext}",
            f"config_setting_id={self.config_setting_id}",
            f"setting={self.setting}",
        ]
        return f"<ConfigSettingEntry [{', '.join(out)}]>"
