# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .contract_data_entry_data import ContractDataEntryData
from .contract_entry_body_type import ContractEntryBodyType

__all__ = ["ContractDataEntryBody"]


class ContractDataEntryBody:
    """
    XDR Source Code::

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
            }
    """

    def __init__(
        self,
        body_type: ContractEntryBodyType,
        data: ContractDataEntryData = None,
    ) -> None:
        self.body_type = body_type
        self.data = data

    def pack(self, packer: Packer) -> None:
        self.body_type.pack(packer)
        if self.body_type == ContractEntryBodyType.DATA_ENTRY:
            if self.data is None:
                raise ValueError("data should not be None.")
            self.data.pack(packer)
            return
        if self.body_type == ContractEntryBodyType.EXPIRATION_EXTENSION:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ContractDataEntryBody:
        body_type = ContractEntryBodyType.unpack(unpacker)
        if body_type == ContractEntryBodyType.DATA_ENTRY:
            data = ContractDataEntryData.unpack(unpacker)
            return cls(body_type=body_type, data=data)
        if body_type == ContractEntryBodyType.EXPIRATION_EXTENSION:
            return cls(body_type=body_type)
        return cls(body_type=body_type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ContractDataEntryBody:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ContractDataEntryBody:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.body_type,
                self.data,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.body_type == other.body_type and self.data == other.data

    def __str__(self):
        out = []
        out.append(f"body_type={self.body_type}")
        out.append(f"data={self.data}") if self.data is not None else None
        return f"<ContractDataEntryBody [{', '.join(out)}]>"
