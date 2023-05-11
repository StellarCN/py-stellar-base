# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib3 import Packer, Unpacker

from .hash import Hash
from .sc_val import SCVal

__all__ = ["LedgerKeyContractData"]


class LedgerKeyContractData:
    """
    XDR Source Code::

        struct
            {
                Hash contractID;
                SCVal key;
            }
    """

    def __init__(
        self,
        contract_id: Hash,
        key: SCVal,
    ) -> None:
        self.contract_id = contract_id
        self.key = key

    def pack(self, packer: Packer) -> None:
        self.contract_id.pack(packer)
        self.key.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerKeyContractData":
        contract_id = Hash.unpack(unpacker)
        key = SCVal.unpack(unpacker)
        return cls(
            contract_id=contract_id,
            key=key,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "LedgerKeyContractData":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerKeyContractData":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.contract_id == other.contract_id and self.key == other.key

    def __str__(self):
        out = [
            f"contract_id={self.contract_id}",
            f"key={self.key}",
        ]
        return f"<LedgerKeyContractData [{', '.join(out)}]>"
