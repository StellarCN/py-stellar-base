# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .base import String
from .constants import *

__all__ = ["SCSpecUDTUnionCaseVoidV0"]


class SCSpecUDTUnionCaseVoidV0:
    """
    XDR Source Code::

        struct SCSpecUDTUnionCaseVoidV0
        {
            string doc<SC_SPEC_DOC_LIMIT>;
            string name<60>;
        };
    """

    def __init__(
        self,
        doc: bytes,
        name: bytes,
    ) -> None:
        self.doc = doc
        self.name = name

    def pack(self, packer: Packer) -> None:
        String(self.doc, SC_SPEC_DOC_LIMIT).pack(packer)
        String(self.name, 60).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCSpecUDTUnionCaseVoidV0:
        doc = String.unpack(unpacker)
        name = String.unpack(unpacker)
        return cls(
            doc=doc,
            name=name,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCSpecUDTUnionCaseVoidV0:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCSpecUDTUnionCaseVoidV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.doc,
                self.name,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.doc == other.doc and self.name == other.name

    def __repr__(self):
        out = [
            f"doc={self.doc}",
            f"name={self.name}",
        ]
        return f"<SCSpecUDTUnionCaseVoidV0 [{', '.join(out)}]>"
