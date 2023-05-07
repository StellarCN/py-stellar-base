# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib3 import Packer, Unpacker

from .config_setting import ConfigSetting
from .config_setting_id import ConfigSettingID

__all__ = ["LedgerUpgradeConfigSetting"]


class LedgerUpgradeConfigSetting:
    """
    XDR Source Code::

        struct
            {
                ConfigSettingID id; // id to update
                ConfigSetting setting; // new value
            }
    """

    def __init__(
        self,
        id: ConfigSettingID,
        setting: ConfigSetting,
    ) -> None:
        self.id = id
        self.setting = setting

    def pack(self, packer: Packer) -> None:
        self.id.pack(packer)
        self.setting.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerUpgradeConfigSetting":
        id = ConfigSettingID.unpack(unpacker)
        setting = ConfigSetting.unpack(unpacker)
        return cls(
            id=id,
            setting=setting,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "LedgerUpgradeConfigSetting":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerUpgradeConfigSetting":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.id == other.id and self.setting == other.setting

    def __str__(self):
        out = [
            f"id={self.id}",
            f"setting={self.setting}",
        ]
        return f"<LedgerUpgradeConfigSetting [{', '.join(out)}]>"
