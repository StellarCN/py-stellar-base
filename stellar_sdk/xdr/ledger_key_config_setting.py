# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .config_setting_id import ConfigSettingID

__all__ = ["LedgerKeyConfigSetting"]


class LedgerKeyConfigSetting:
    """
    XDR Source Code::

        struct
            {
                ConfigSettingID configSettingID;
            }
    """

    def __init__(
        self,
        config_setting_id: ConfigSettingID,
    ) -> None:
        self.config_setting_id = config_setting_id

    def pack(self, packer: Packer) -> None:
        self.config_setting_id.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> LedgerKeyConfigSetting:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        config_setting_id = ConfigSettingID.unpack(unpacker)
        return cls(
            config_setting_id=config_setting_id,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerKeyConfigSetting:
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
    def from_xdr(cls, xdr: str) -> LedgerKeyConfigSetting:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LedgerKeyConfigSetting:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "config_setting_id": self.config_setting_id.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> LedgerKeyConfigSetting:
        config_setting_id = ConfigSettingID.from_json_dict(
            json_dict["config_setting_id"]
        )
        return cls(
            config_setting_id=config_setting_id,
        )

    def __hash__(self):
        return hash((self.config_setting_id,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.config_setting_id == other.config_setting_id

    def __repr__(self):
        out = [
            f"config_setting_id={self.config_setting_id}",
        ]
        return f"<LedgerKeyConfigSetting [{', '.join(out)}]>"
