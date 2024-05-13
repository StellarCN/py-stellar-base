# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import String
from .constants import *
from .sc_spec_type_def import SCSpecTypeDef

__all__ = ["SCSpecUDTUnionCaseTupleV0"]


class SCSpecUDTUnionCaseTupleV0:
    """
    XDR Source Code::

        struct SCSpecUDTUnionCaseTupleV0
        {
            string doc<SC_SPEC_DOC_LIMIT>;
            string name<60>;
            SCSpecTypeDef type<12>;
        };
    """

    def __init__(
        self,
        doc: bytes,
        name: bytes,
        type: List[SCSpecTypeDef],
    ) -> None:
        _expect_max_length = 12
        if type and len(type) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `type` should be {_expect_max_length}, but got {len(type)}."
            )
        self.doc = doc
        self.name = name
        self.type = type

    def pack(self, packer: Packer) -> None:
        String(self.doc, SC_SPEC_DOC_LIMIT).pack(packer)
        String(self.name, 60).pack(packer)
        packer.pack_uint(len(self.type))
        for type_item in self.type:
            type_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCSpecUDTUnionCaseTupleV0:
        doc = String.unpack(unpacker)
        name = String.unpack(unpacker)
        length = unpacker.unpack_uint()
        type = []
        for _ in range(length):
            type.append(SCSpecTypeDef.unpack(unpacker))
        return cls(
            doc=doc,
            name=name,
            type=type,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCSpecUDTUnionCaseTupleV0:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCSpecUDTUnionCaseTupleV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.doc,
                self.name,
                self.type,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.doc == other.doc
            and self.name == other.name
            and self.type == other.type
        )

    def __repr__(self):
        out = [
            f"doc={self.doc}",
            f"name={self.name}",
            f"type={self.type}",
        ]
        return f"<SCSpecUDTUnionCaseTupleV0 [{', '.join(out)}]>"
