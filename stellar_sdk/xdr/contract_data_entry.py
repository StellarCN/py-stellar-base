# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .contract_data_durability import ContractDataDurability
from .extension_point import ExtensionPoint
from .sc_address import SCAddress
from .sc_val import SCVal

__all__ = ["ContractDataEntry"]


class ContractDataEntry:
    """
    XDR Source Code::

        struct ContractDataEntry {
            ExtensionPoint ext;

            SCAddress contract;
            SCVal key;
            ContractDataDurability durability;
            SCVal val;
        };
    """

    def __init__(
        self,
        ext: ExtensionPoint,
        contract: SCAddress,
        key: SCVal,
        durability: ContractDataDurability,
        val: SCVal,
    ) -> None:
        self.ext = ext
        self.contract = contract
        self.key = key
        self.durability = durability
        self.val = val

    def pack(self, packer: Packer) -> None:
        self.ext.pack(packer)
        self.contract.pack(packer)
        self.key.pack(packer)
        self.durability.pack(packer)
        self.val.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ContractDataEntry:
        ext = ExtensionPoint.unpack(unpacker)
        contract = SCAddress.unpack(unpacker)
        key = SCVal.unpack(unpacker)
        durability = ContractDataDurability.unpack(unpacker)
        val = SCVal.unpack(unpacker)
        return cls(
            ext=ext,
            contract=contract,
            key=key,
            durability=durability,
            val=val,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ContractDataEntry:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ContractDataEntry:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.ext,
                self.contract,
                self.key,
                self.durability,
                self.val,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ext == other.ext
            and self.contract == other.contract
            and self.key == other.key
            and self.durability == other.durability
            and self.val == other.val
        )

    def __repr__(self):
        out = [
            f"ext={self.ext}",
            f"contract={self.contract}",
            f"key={self.key}",
            f"durability={self.durability}",
            f"val={self.val}",
        ]
        return f"<ContractDataEntry [{', '.join(out)}]>"
