# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .contract_data_durability import ContractDataDurability
from .contract_entry_body_type import ContractEntryBodyType
from .sc_address import SCAddress
from .sc_val import SCVal

__all__ = ["LedgerKeyContractData"]


class LedgerKeyContractData:
    """
    XDR Source Code::

        struct
            {
                SCAddress contract;
                SCVal key;
                ContractDataDurability durability;
                ContractEntryBodyType bodyType;
            }
    """

    def __init__(
        self,
        contract: SCAddress,
        key: SCVal,
        durability: ContractDataDurability,
        body_type: ContractEntryBodyType,
    ) -> None:
        self.contract = contract
        self.key = key
        self.durability = durability
        self.body_type = body_type

    def pack(self, packer: Packer) -> None:
        self.contract.pack(packer)
        self.key.pack(packer)
        self.durability.pack(packer)
        self.body_type.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> LedgerKeyContractData:
        contract = SCAddress.unpack(unpacker)
        key = SCVal.unpack(unpacker)
        durability = ContractDataDurability.unpack(unpacker)
        body_type = ContractEntryBodyType.unpack(unpacker)
        return cls(
            contract=contract,
            key=key,
            durability=durability,
            body_type=body_type,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerKeyContractData:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LedgerKeyContractData:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.contract,
                self.key,
                self.durability,
                self.body_type,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.contract == other.contract
            and self.key == other.key
            and self.durability == other.durability
            and self.body_type == other.body_type
        )

    def __str__(self):
        out = [
            f"contract={self.contract}",
            f"key={self.key}",
            f"durability={self.durability}",
            f"body_type={self.body_type}",
        ]
        return f"<LedgerKeyContractData [{', '.join(out)}]>"
