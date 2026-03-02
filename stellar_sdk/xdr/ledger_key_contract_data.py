# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .contract_data_durability import ContractDataDurability
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
            }
    """

    def __init__(
        self,
        contract: SCAddress,
        key: SCVal,
        durability: ContractDataDurability,
    ) -> None:
        self.contract = contract
        self.key = key
        self.durability = durability

    def pack(self, packer: Packer) -> None:
        self.contract.pack(packer)
        self.key.pack(packer)
        self.durability.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> LedgerKeyContractData:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        contract = SCAddress.unpack(unpacker, depth_limit - 1)
        key = SCVal.unpack(unpacker, depth_limit - 1)
        durability = ContractDataDurability.unpack(unpacker)
        return cls(
            contract=contract,
            key=key,
            durability=durability,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerKeyContractData:
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
    def from_xdr(cls, xdr: str) -> LedgerKeyContractData:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LedgerKeyContractData:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "contract": self.contract.to_json_dict(),
            "key": self.key.to_json_dict(),
            "durability": self.durability.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> LedgerKeyContractData:
        contract = SCAddress.from_json_dict(json_dict["contract"])
        key = SCVal.from_json_dict(json_dict["key"])
        durability = ContractDataDurability.from_json_dict(json_dict["durability"])
        return cls(
            contract=contract,
            key=key,
            durability=durability,
        )

    def __hash__(self):
        return hash(
            (
                self.contract,
                self.key,
                self.durability,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.contract == other.contract
            and self.key == other.key
            and self.durability == other.durability
        )

    def __repr__(self):
        out = [
            f"contract={self.contract}",
            f"key={self.key}",
            f"durability={self.durability}",
        ]
        return f"<LedgerKeyContractData [{', '.join(out)}]>"
