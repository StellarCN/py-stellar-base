# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .int64 import Int64

__all__ = ["ConfigSettingContractHistoricalDataV0"]


class ConfigSettingContractHistoricalDataV0:
    """
    XDR Source Code::

        struct ConfigSettingContractHistoricalDataV0
        {
            int64 feeHistorical1KB; // Fee for storing 1KB in archives
        };
    """

    def __init__(
        self,
        fee_historical1_kb: Int64,
    ) -> None:
        self.fee_historical1_kb = fee_historical1_kb

    def pack(self, packer: Packer) -> None:
        self.fee_historical1_kb.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ConfigSettingContractHistoricalDataV0:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        fee_historical1_kb = Int64.unpack(unpacker, depth_limit - 1)
        return cls(
            fee_historical1_kb=fee_historical1_kb,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ConfigSettingContractHistoricalDataV0:
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
    def from_xdr(cls, xdr: str) -> ConfigSettingContractHistoricalDataV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ConfigSettingContractHistoricalDataV0:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "fee_historical1_kb": self.fee_historical1_kb.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> ConfigSettingContractHistoricalDataV0:
        fee_historical1_kb = Int64.from_json_dict(json_dict["fee_historical1_kb"])
        return cls(
            fee_historical1_kb=fee_historical1_kb,
        )

    def __hash__(self):
        return hash((self.fee_historical1_kb,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.fee_historical1_kb == other.fee_historical1_kb

    def __repr__(self):
        out = [
            f"fee_historical1_kb={self.fee_historical1_kb}",
        ]
        return f"<ConfigSettingContractHistoricalDataV0 [{', '.join(out)}]>"
