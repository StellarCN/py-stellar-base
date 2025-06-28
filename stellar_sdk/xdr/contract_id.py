# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .hash import Hash

__all__ = ["ContractID"]


class ContractID:
    """
    XDR Source Code::

        typedef Hash ContractID;
    """

    def __init__(self, contract_id: Hash) -> None:
        self.contract_id = contract_id

    def pack(self, packer: Packer) -> None:
        self.contract_id.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ContractID:
        contract_id = Hash.unpack(unpacker)
        return cls(contract_id)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ContractID:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ContractID:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(self.contract_id)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.contract_id == other.contract_id

    def __repr__(self):
        return f"<ContractID [contract_id={self.contract_id}]>"
