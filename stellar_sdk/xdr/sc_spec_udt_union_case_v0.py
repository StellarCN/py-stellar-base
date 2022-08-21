# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import Optional
from xdrlib import Packer, Unpacker

from .base import String
from .sc_spec_type_def import SCSpecTypeDef

__all__ = ["SCSpecUDTUnionCaseV0"]


class SCSpecUDTUnionCaseV0:
    """
    XDR Source Code::

        struct SCSpecUDTUnionCaseV0
        {
            string name<60>;
            SCSpecTypeDef *type;
        };
    """

    def __init__(
        self,
        name: bytes,
        type: Optional[SCSpecTypeDef],
    ) -> None:
        self.name = name
        self.type = type

    def pack(self, packer: Packer) -> None:
        String(self.name, 60).pack(packer)
        if self.type is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.type.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCSpecUDTUnionCaseV0":
        name = String.unpack(unpacker)
        type = SCSpecTypeDef.unpack(unpacker) if unpacker.unpack_uint() else None
        return cls(
            name=name,
            type=type,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCSpecUDTUnionCaseV0":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCSpecUDTUnionCaseV0":
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
        return f"<SCSpecUDTUnionCaseV0 [{', '.join(out)}]>"
