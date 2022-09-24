# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .base import String
from .sc_spec_type_def import SCSpecTypeDef

__all__ = ["SCSpecFunctionInputV0"]


class SCSpecFunctionInputV0:
    """
    XDR Source Code::

        struct SCSpecFunctionInputV0
        {
            string name<30>;
            SCSpecTypeDef type;
        };
    """

    def __init__(
        self,
        name: bytes,
        type: SCSpecTypeDef,
    ) -> None:
        self.name = name
        self.type = type

    def pack(self, packer: Packer) -> None:
        String(self.name, 30).pack(packer)
        self.type.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCSpecFunctionInputV0":
        name = String.unpack(unpacker)
        type = SCSpecTypeDef.unpack(unpacker)
        return cls(
            name=name,
            type=type,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCSpecFunctionInputV0":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCSpecFunctionInputV0":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.name == other.name and self.type == other.type

    def __str__(self):
        out = [
            f"name={self.name}",
            f"type={self.type}",
        ]
        return f"<SCSpecFunctionInputV0 [{', '.join(out)}]>"
