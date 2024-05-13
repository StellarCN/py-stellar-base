# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .sc_spec_type_def import SCSpecTypeDef

__all__ = ["SCSpecTypeVec"]


class SCSpecTypeVec:
    """
    XDR Source Code::

        struct SCSpecTypeVec
        {
            SCSpecTypeDef elementType;
        };
    """

    def __init__(
        self,
        element_type: SCSpecTypeDef,
    ) -> None:
        self.element_type = element_type

    def pack(self, packer: Packer) -> None:
        self.element_type.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCSpecTypeVec:
        element_type = SCSpecTypeDef.unpack(unpacker)
        return cls(
            element_type=element_type,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCSpecTypeVec:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCSpecTypeVec:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash((self.element_type,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.element_type == other.element_type

    def __repr__(self):
        out = [
            f"element_type={self.element_type}",
        ]
        return f"<SCSpecTypeVec [{', '.join(out)}]>"
