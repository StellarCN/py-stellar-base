# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import Optional
from xdrlib import Packer, Unpacker

from .data_value import DataValue
from .string64 import String64

__all__ = ["ManageDataOp"]


class ManageDataOp:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct ManageDataOp
    {
        string64 dataName;
        DataValue* dataValue; // set to null to clear
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        data_name: String64,
        data_value: Optional[DataValue],
    ) -> None:
        self.data_name = data_name
        self.data_value = data_value

    def pack(self, packer: Packer) -> None:
        self.data_name.pack(packer)
        if self.data_value is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.data_value.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ManageDataOp":
        data_name = String64.unpack(unpacker)
        data_value = DataValue.unpack(unpacker) if unpacker.unpack_uint() else None
        return cls(
            data_name=data_name,
            data_value=data_value,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "ManageDataOp":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ManageDataOp":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.data_name == other.data_name and self.data_value == other.data_value

    def __str__(self):
        out = [
            f"data_name={self.data_name}",
            f"data_value={self.data_value}",
        ]
        return f"<ManageDataOp {[', '.join(out)]}>"
