# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, String
from .constants import *
from .sc_spec_udt_error_enum_case_v0 import SCSpecUDTErrorEnumCaseV0

__all__ = ["SCSpecUDTErrorEnumV0"]


class SCSpecUDTErrorEnumV0:
    """
    XDR Source Code::

        struct SCSpecUDTErrorEnumV0
        {
            string doc<SC_SPEC_DOC_LIMIT>;
            string lib<80>;
            string name<60>;
            SCSpecUDTErrorEnumCaseV0 cases<50>;
        };
    """

    def __init__(
        self,
        doc: bytes,
        lib: bytes,
        name: bytes,
        cases: List[SCSpecUDTErrorEnumCaseV0],
    ) -> None:
        _expect_max_length = SC_SPEC_DOC_LIMIT
        if doc and len(doc) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `doc` should be {_expect_max_length}, but got {len(doc)}."
            )
        _expect_max_length = 80
        if lib and len(lib) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `lib` should be {_expect_max_length}, but got {len(lib)}."
            )
        _expect_max_length = 60
        if name and len(name) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `name` should be {_expect_max_length}, but got {len(name)}."
            )
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCSpecUDTErrorEnumV0:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        doc = String.unpack(unpacker, SC_SPEC_DOC_LIMIT)
        lib = String.unpack(unpacker, 80)
        name = String.unpack(unpacker, 60)
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"cases length {length} exceeds remaining input length {_remaining}"
            )
        cases = []
        for _ in range(length):
            cases.append(SCSpecUDTErrorEnumCaseV0.unpack(unpacker, depth_limit - 1))
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
    def from_xdr_bytes(cls, xdr: bytes) -> SCSpecUDTErrorEnumV0:
        unpacker = Unpacker(xdr)
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCSpecUDTErrorEnumV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCSpecUDTErrorEnumV0:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "doc": String.to_json_dict(self.doc),
            "lib": String.to_json_dict(self.lib),
            "name": String.to_json_dict(self.name),
            "cases": [item.to_json_dict() for item in self.cases],
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SCSpecUDTErrorEnumV0:
        doc = String.from_json_dict(json_dict["doc"])
        lib = String.from_json_dict(json_dict["lib"])
        name = String.from_json_dict(json_dict["name"])
        cases = [
            SCSpecUDTErrorEnumCaseV0.from_json_dict(item) for item in json_dict["cases"]
        ]
        return cls(
            doc=doc,
            lib=lib,
            name=name,
            cases=cases,
        )

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
        return f"<SCSpecUDTErrorEnumV0 [{', '.join(out)}]>"
