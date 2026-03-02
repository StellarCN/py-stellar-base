# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, String
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
        self.doc = doc
        self.name = name
        self.value = value

    def pack(self, packer: Packer) -> None:
        String(self.doc, SC_SPEC_DOC_LIMIT).pack(packer)
        String(self.name, 60).pack(packer)
        self.value.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCSpecUDTErrorEnumCaseV0:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        doc = String.unpack(unpacker, SC_SPEC_DOC_LIMIT)
        name = String.unpack(unpacker, 60)
        value = Uint32.unpack(unpacker, depth_limit - 1)
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCSpecUDTErrorEnumCaseV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCSpecUDTErrorEnumCaseV0:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "doc": String.to_json_dict(self.doc),
            "name": String.to_json_dict(self.name),
            "value": self.value.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SCSpecUDTErrorEnumCaseV0:
        doc = String.from_json_dict(json_dict["doc"])
        name = String.from_json_dict(json_dict["name"])
        value = Uint32.from_json_dict(json_dict["value"])
        return cls(
            doc=doc,
            name=name,
            value=value,
        )

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
