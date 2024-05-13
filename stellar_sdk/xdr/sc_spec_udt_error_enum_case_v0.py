# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .base import String
from .constants import *
from .uint32 import Uint32

__all__ = ["SCSpecUDTErrorEnumCaseV0"]


class SCSpecUDTErrorEnumCaseV0:
    """
    XDR Source Code::

        struct SCSpecUDTErrorEnumCaseV0
        {
            string doc<SC_SPEC_DOC_LIMIT>;
            string name<60>;
            uint32 value;
        };
    """

    def __init__(
        self,
        doc: bytes,
        name: bytes,
        value: Uint32,
    ) -> None:
        self.doc = doc
        self.name = name
        self.value = value

    def pack(self, packer: Packer) -> None:
        String(self.doc, SC_SPEC_DOC_LIMIT).pack(packer)
        String(self.name, 60).pack(packer)
        self.value.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCSpecUDTErrorEnumCaseV0:
        doc = String.unpack(unpacker)
        name = String.unpack(unpacker)
        value = Uint32.unpack(unpacker)
        return cls(
            doc=doc,
            name=name,
            value=value,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCSpecUDTErrorEnumCaseV0:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCSpecUDTErrorEnumCaseV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.doc,
                self.name,
                self.value,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.doc == other.doc
            and self.name == other.name
            and self.value == other.value
        )

    def __repr__(self):
        out = [
            f"doc={self.doc}",
            f"name={self.name}",
            f"value={self.value}",
        ]
        return f"<SCSpecUDTErrorEnumCaseV0 [{', '.join(out)}]>"
