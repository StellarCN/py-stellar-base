# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, String
from .constants import *
from .sc_spec_event_data_format import SCSpecEventDataFormat
from .sc_spec_event_param_v0 import SCSpecEventParamV0
from .sc_symbol import SCSymbol

__all__ = ["SCSpecEventV0"]


class SCSpecEventV0:
    """
    XDR Source Code::

        struct SCSpecEventV0
        {
            string doc<SC_SPEC_DOC_LIMIT>;
            string lib<80>;
            SCSymbol name;
            SCSymbol prefixTopics<2>;
            SCSpecEventParamV0 params<50>;
            SCSpecEventDataFormat dataFormat;
        };
    """

    def __init__(
        self,
        doc: bytes,
        lib: bytes,
        name: SCSymbol,
        prefix_topics: List[SCSymbol],
        params: List[SCSpecEventParamV0],
        data_format: SCSpecEventDataFormat,
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
        _expect_max_length = 2
        if prefix_topics and len(prefix_topics) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `prefix_topics` should be {_expect_max_length}, but got {len(prefix_topics)}."
            )
        _expect_max_length = 50
        if params and len(params) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `params` should be {_expect_max_length}, but got {len(params)}."
            )
        self.doc = doc
        self.lib = lib
        self.name = name
        self.prefix_topics = prefix_topics
        self.params = params
        self.data_format = data_format

    def pack(self, packer: Packer) -> None:
        String(self.doc, SC_SPEC_DOC_LIMIT).pack(packer)
        String(self.lib, 80).pack(packer)
        self.name.pack(packer)
        packer.pack_uint(len(self.prefix_topics))
        for prefix_topics_item in self.prefix_topics:
            prefix_topics_item.pack(packer)
        packer.pack_uint(len(self.params))
        for params_item in self.params:
            params_item.pack(packer)
        self.data_format.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCSpecEventV0:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        doc = String.unpack(unpacker, SC_SPEC_DOC_LIMIT)
        lib = String.unpack(unpacker, 80)
        name = SCSymbol.unpack(unpacker, depth_limit - 1)
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"prefix_topics length {length} exceeds remaining input length {_remaining}"
            )
        prefix_topics = []
        for _ in range(length):
            prefix_topics.append(SCSymbol.unpack(unpacker, depth_limit - 1))
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"params length {length} exceeds remaining input length {_remaining}"
            )
        params = []
        for _ in range(length):
            params.append(SCSpecEventParamV0.unpack(unpacker, depth_limit - 1))
        data_format = SCSpecEventDataFormat.unpack(unpacker)
        return cls(
            doc=doc,
            lib=lib,
            name=name,
            prefix_topics=prefix_topics,
            params=params,
            data_format=data_format,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCSpecEventV0:
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
    def from_xdr(cls, xdr: str) -> SCSpecEventV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCSpecEventV0:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "doc": String.to_json_dict(self.doc),
            "lib": String.to_json_dict(self.lib),
            "name": self.name.to_json_dict(),
            "prefix_topics": [item.to_json_dict() for item in self.prefix_topics],
            "params": [item.to_json_dict() for item in self.params],
            "data_format": self.data_format.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SCSpecEventV0:
        doc = String.from_json_dict(json_dict["doc"])
        lib = String.from_json_dict(json_dict["lib"])
        name = SCSymbol.from_json_dict(json_dict["name"])
        prefix_topics = [
            SCSymbol.from_json_dict(item) for item in json_dict["prefix_topics"]
        ]
        params = [
            SCSpecEventParamV0.from_json_dict(item) for item in json_dict["params"]
        ]
        data_format = SCSpecEventDataFormat.from_json_dict(json_dict["data_format"])
        return cls(
            doc=doc,
            lib=lib,
            name=name,
            prefix_topics=prefix_topics,
            params=params,
            data_format=data_format,
        )

    def __hash__(self):
        return hash(
            (
                self.doc,
                self.lib,
                self.name,
                self.prefix_topics,
                self.params,
                self.data_format,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.doc == other.doc
            and self.lib == other.lib
            and self.name == other.name
            and self.prefix_topics == other.prefix_topics
            and self.params == other.params
            and self.data_format == other.data_format
        )

    def __repr__(self):
        out = [
            f"doc={self.doc}",
            f"lib={self.lib}",
            f"name={self.name}",
            f"prefix_topics={self.prefix_topics}",
            f"params={self.params}",
            f"data_format={self.data_format}",
        ]
        return f"<SCSpecEventV0 [{', '.join(out)}]>"
