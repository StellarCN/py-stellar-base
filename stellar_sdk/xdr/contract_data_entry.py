# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .contract_data_durability import ContractDataDurability
from .contract_data_entry_body import ContractDataEntryBody
from .sc_address import SCAddress
from .sc_val import SCVal
from .uint32 import Uint32

__all__ = ["ContractDataEntry"]


class ContractDataEntry:
    """
    XDR Source Code::

        struct ContractDataEntry {
            SCAddress contract;
            SCVal key;
            ContractDataDurability durability;

            union switch (ContractEntryBodyType bodyType)
            {
            case DATA_ENTRY:
            struct
            {
                uint32 flags;
                SCVal val;
            } data;
            case EXPIRATION_EXTENSION:
                void;
            } body;

            uint32 expirationLedgerSeq;
        };
    """

    def __init__(
        self,
        contract: SCAddress,
        key: SCVal,
        durability: ContractDataDurability,
        body: ContractDataEntryBody,
        expiration_ledger_seq: Uint32,
    ) -> None:
        self.contract = contract
        self.key = key
        self.durability = durability
        self.body = body
        self.expiration_ledger_seq = expiration_ledger_seq

    def pack(self, packer: Packer) -> None:
        self.contract.pack(packer)
        self.key.pack(packer)
        self.durability.pack(packer)
        self.body.pack(packer)
        self.expiration_ledger_seq.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ContractDataEntry:
        contract = SCAddress.unpack(unpacker)
        key = SCVal.unpack(unpacker)
        durability = ContractDataDurability.unpack(unpacker)
        body = ContractDataEntryBody.unpack(unpacker)
        expiration_ledger_seq = Uint32.unpack(unpacker)
        return cls(
            contract=contract,
            key=key,
            durability=durability,
            body=body,
            expiration_ledger_seq=expiration_ledger_seq,
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
                self.contract,
                self.key,
                self.durability,
                self.body,
                self.expiration_ledger_seq,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.contract == other.contract
            and self.key == other.key
            and self.durability == other.durability
            and self.body == other.body
            and self.expiration_ledger_seq == other.expiration_ledger_seq
        )

    def __str__(self):
        out = [
            f"contract={self.contract}",
            f"key={self.key}",
            f"durability={self.durability}",
            f"body={self.body}",
            f"expiration_ledger_seq={self.expiration_ledger_seq}",
        ]
        return f"<ContractDataEntry [{', '.join(out)}]>"
