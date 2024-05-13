# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

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
    def unpack(cls, unpacker: Unpacker) -> ConfigSettingContractHistoricalDataV0:
        fee_historical1_kb = Int64.unpack(unpacker)
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
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ConfigSettingContractHistoricalDataV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
