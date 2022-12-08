# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .contract_id import ContractID
from .sc_contract_code import SCContractCode

__all__ = ["CreateContractArgs"]


class CreateContractArgs:
    """
    XDR Source Code::

        struct CreateContractArgs
        {
            ContractID contractID;
            SCContractCode source;
        };
    """

    def __init__(
        self,
        contract_id: ContractID,
        source: SCContractCode,
    ) -> None:
        self.contract_id = contract_id
        self.source = source

    def pack(self, packer: Packer) -> None:
        self.contract_id.pack(packer)
        self.source.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "CreateContractArgs":
        contract_id = ContractID.unpack(unpacker)
        source = SCContractCode.unpack(unpacker)
        return cls(
            contract_id=contract_id,
            source=source,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "CreateContractArgs":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "CreateContractArgs":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.contract_id == other.contract_id and self.source == other.source

    def __str__(self):
        out = [
            f"contract_id={self.contract_id}",
            f"source={self.source}",
        ]
        return f"<CreateContractArgs [{', '.join(out)}]>"
