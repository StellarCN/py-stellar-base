# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .int64 import Int64
from .uint32 import Uint32

__all__ = ["ConfigSettingContractMetaDataV0"]


class ConfigSettingContractMetaDataV0:
    """
    XDR Source Code::

        struct ConfigSettingContractMetaDataV0
        {
            // Maximum size of extended meta data produced by a transaction
            uint32 txMaxExtendedMetaDataSizeBytes;
            // Fee for generating 1KB of extended meta data
            int64 feeExtendedMetaData1KB;
        };
    """

    def __init__(
        self,
        tx_max_extended_meta_data_size_bytes: Uint32,
        fee_extended_meta_data1_kb: Int64,
    ) -> None:
        self.tx_max_extended_meta_data_size_bytes = tx_max_extended_meta_data_size_bytes
        self.fee_extended_meta_data1_kb = fee_extended_meta_data1_kb

    def pack(self, packer: Packer) -> None:
        self.tx_max_extended_meta_data_size_bytes.pack(packer)
        self.fee_extended_meta_data1_kb.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ConfigSettingContractMetaDataV0:
        tx_max_extended_meta_data_size_bytes = Uint32.unpack(unpacker)
        fee_extended_meta_data1_kb = Int64.unpack(unpacker)
        return cls(
            tx_max_extended_meta_data_size_bytes=tx_max_extended_meta_data_size_bytes,
            fee_extended_meta_data1_kb=fee_extended_meta_data1_kb,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ConfigSettingContractMetaDataV0:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ConfigSettingContractMetaDataV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.tx_max_extended_meta_data_size_bytes,
                self.fee_extended_meta_data1_kb,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.tx_max_extended_meta_data_size_bytes
            == other.tx_max_extended_meta_data_size_bytes
            and self.fee_extended_meta_data1_kb == other.fee_extended_meta_data1_kb
        )

    def __str__(self):
        out = [
            f"tx_max_extended_meta_data_size_bytes={self.tx_max_extended_meta_data_size_bytes}",
            f"fee_extended_meta_data1_kb={self.fee_extended_meta_data1_kb}",
        ]
        return f"<ConfigSettingContractMetaDataV0 [{', '.join(out)}]>"
