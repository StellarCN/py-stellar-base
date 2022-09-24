# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .base import String
from .uint32 import Uint32

__all__ = ["SCSpecUDTErrorEnumCaseV0"]


class SCSpecUDTErrorEnumCaseV0:
    """
    XDR Source Code::

        struct SCSpecUDTErrorEnumCaseV0
        {
            string name<60>;
            uint32 value;
        };
    """

    def __init__(
        self,
        name: bytes,
        value: Uint32,
    ) -> None:
        self.name = name
        self.value = value

    def pack(self, packer: Packer) -> None:
        String(self.name, 60).pack(packer)
        self.value.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCSpecUDTErrorEnumCaseV0":
        name = String.unpack(unpacker)
        value = Uint32.unpack(unpacker)
        return cls(
            name=name,
            value=value,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCSpecUDTErrorEnumCaseV0":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCSpecUDTErrorEnumCaseV0":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.name == other.name and self.value == other.value

    def __str__(self):
        out = [
            f"name={self.name}",
            f"value={self.value}",
        ]
        return f"<SCSpecUDTErrorEnumCaseV0 [{', '.join(out)}]>"
