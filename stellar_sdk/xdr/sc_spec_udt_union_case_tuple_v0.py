# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, String
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
            SCSpecTypeDef type<>;
        };
    """

    def __init__(
        self,
        doc: bytes,
        name: bytes,
        type: List[SCSpecTypeDef],
    ) -> None:
        _expect_max_length = SC_SPEC_DOC_LIMIT
        if doc and len(doc) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `doc` should be {_expect_max_length}, but got {len(doc)}."
            )
        _expect_max_length = 60
        if name and len(name) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `name` should be {_expect_max_length}, but got {len(name)}."
            )
        _expect_max_length = 4294967295
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCSpecUDTUnionCaseTupleV0:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        doc = String.unpack(unpacker, SC_SPEC_DOC_LIMIT)
        name = String.unpack(unpacker, 60)
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"type length {length} exceeds remaining input length {_remaining}"
            )
        type = []
        for _ in range(length):
            type.append(SCSpecTypeDef.unpack(unpacker, depth_limit - 1))
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCSpecUDTUnionCaseTupleV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCSpecUDTUnionCaseTupleV0:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "doc": String.to_json_dict(self.doc),
            "name": String.to_json_dict(self.name),
            "type": [item.to_json_dict() for item in self.type],
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SCSpecUDTUnionCaseTupleV0:
        doc = String.from_json_dict(json_dict["doc"])
        name = String.from_json_dict(json_dict["name"])
        type = [SCSpecTypeDef.from_json_dict(item) for item in json_dict["type"]]
        return cls(
            doc=doc,
            name=name,
            type=type,
        )

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
