# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import String
from .constants import *
from .sc_spec_udt_union_case_v0 import SCSpecUDTUnionCaseV0

__all__ = ["SCSpecUDTUnionV0"]


class SCSpecUDTUnionV0:
    """
    XDR Source Code::

        struct SCSpecUDTUnionV0
        {
            string doc<SC_SPEC_DOC_LIMIT>;
            string lib<80>;
            string name<60>;
            SCSpecUDTUnionCaseV0 cases<50>;
        };
    """

    def __init__(
        self,
        doc: bytes,
        lib: bytes,
        name: bytes,
        cases: List[SCSpecUDTUnionCaseV0],
    ) -> None:
        _expect_max_length = 50
        if cases and len(cases) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `cases` should be {_expect_max_length}, but got {len(cases)}."
            )
        self.doc = doc
        self.lib = lib
        self.name = name
        self.cases = cases

    def pack(self, packer: Packer) -> None:
        String(self.doc, SC_SPEC_DOC_LIMIT).pack(packer)
        String(self.lib, 80).pack(packer)
        String(self.name, 60).pack(packer)
        packer.pack_uint(len(self.cases))
        for cases_item in self.cases:
            cases_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCSpecUDTUnionV0:
        doc = String.unpack(unpacker)
        lib = String.unpack(unpacker)
        name = String.unpack(unpacker)
        length = unpacker.unpack_uint()
        cases = []
        for _ in range(length):
            cases.append(SCSpecUDTUnionCaseV0.unpack(unpacker))
        return cls(
            doc=doc,
            lib=lib,
            name=name,
            cases=cases,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCSpecUDTUnionV0:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCSpecUDTUnionV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.doc,
                self.lib,
                self.name,
                self.cases,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.doc == other.doc
            and self.lib == other.lib
            and self.name == other.name
            and self.cases == other.cases
        )

    def __repr__(self):
        out = [
            f"doc={self.doc}",
            f"lib={self.lib}",
            f"name={self.name}",
            f"cases={self.cases}",
        ]
        return f"<SCSpecUDTUnionV0 [{', '.join(out)}]>"
