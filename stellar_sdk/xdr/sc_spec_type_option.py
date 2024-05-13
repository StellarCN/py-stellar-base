# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .sc_spec_type_def import SCSpecTypeDef

__all__ = ["SCSpecTypeOption"]


class SCSpecTypeOption:
    """
    XDR Source Code::

        struct SCSpecTypeOption
        {
            SCSpecTypeDef valueType;
        };
    """

    def __init__(
        self,
        value_type: SCSpecTypeDef,
    ) -> None:
        self.value_type = value_type

    def pack(self, packer: Packer) -> None:
        self.value_type.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCSpecTypeOption:
        value_type = SCSpecTypeDef.unpack(unpacker)
        return cls(
            value_type=value_type,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCSpecTypeOption:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCSpecTypeOption:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash((self.value_type,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value_type == other.value_type

    def __repr__(self):
        out = [
            f"value_type={self.value_type}",
        ]
        return f"<SCSpecTypeOption [{', '.join(out)}]>"
