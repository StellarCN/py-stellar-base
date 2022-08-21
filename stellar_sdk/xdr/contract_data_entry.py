# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .hash import Hash
from .sc_val import SCVal

__all__ = ["ContractDataEntry"]


class ContractDataEntry:
    """
    XDR Source Code::

        struct ContractDataEntry {
            Hash contractID;
            SCVal key;
            SCVal val;
        };
    """

    def __init__(
        self,
        contract_id: Hash,
        key: SCVal,
        val: SCVal,
    ) -> None:
        self.contract_id = contract_id
        self.key = key
        self.val = val

    def pack(self, packer: Packer) -> None:
        self.contract_id.pack(packer)
        self.key.pack(packer)
        self.val.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ContractDataEntry":
        contract_id = Hash.unpack(unpacker)
        key = SCVal.unpack(unpacker)
        val = SCVal.unpack(unpacker)
        return cls(
            contract_id=contract_id,
            key=key,
            val=val,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "ContractDataEntry":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ContractDataEntry":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.contract_id == other.contract_id
            and self.key == other.key
            and self.val == other.val
        )

    def __str__(self):
        out = [
            f"contract_id={self.contract_id}",
            f"key={self.key}",
            f"val={self.val}",
        ]
        return f"<ContractDataEntry [{', '.join(out)}]>"
