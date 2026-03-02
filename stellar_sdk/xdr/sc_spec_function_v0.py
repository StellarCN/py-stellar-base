# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, String
from .constants import *
from .sc_spec_function_input_v0 import SCSpecFunctionInputV0
from .sc_spec_type_def import SCSpecTypeDef
from .sc_symbol import SCSymbol

__all__ = ["SCSpecFunctionV0"]


class SCSpecFunctionV0:
    """
    XDR Source Code::

        struct SCSpecFunctionV0
        {
            string doc<SC_SPEC_DOC_LIMIT>;
            SCSymbol name;
            SCSpecFunctionInputV0 inputs<>;
            SCSpecTypeDef outputs<1>;
        };
    """

    def __init__(
        self,
        doc: bytes,
        name: SCSymbol,
        inputs: List[SCSpecFunctionInputV0],
        outputs: List[SCSpecTypeDef],
    ) -> None:
        _expect_max_length = SC_SPEC_DOC_LIMIT
        if doc and len(doc) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `doc` should be {_expect_max_length}, but got {len(doc)}."
            )
        _expect_max_length = 4294967295
        if inputs and len(inputs) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `inputs` should be {_expect_max_length}, but got {len(inputs)}."
            )
        _expect_max_length = 1
        if outputs and len(outputs) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `outputs` should be {_expect_max_length}, but got {len(outputs)}."
            )
        self.doc = doc
        self.name = name
        self.inputs = inputs
        self.outputs = outputs

    def pack(self, packer: Packer) -> None:
        String(self.doc, SC_SPEC_DOC_LIMIT).pack(packer)
        self.name.pack(packer)
        packer.pack_uint(len(self.inputs))
        for inputs_item in self.inputs:
            inputs_item.pack(packer)
        packer.pack_uint(len(self.outputs))
        for outputs_item in self.outputs:
            outputs_item.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCSpecFunctionV0:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        doc = String.unpack(unpacker, SC_SPEC_DOC_LIMIT)
        name = SCSymbol.unpack(unpacker, depth_limit - 1)
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"inputs length {length} exceeds remaining input length {_remaining}"
            )
        inputs = []
        for _ in range(length):
            inputs.append(SCSpecFunctionInputV0.unpack(unpacker, depth_limit - 1))
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"outputs length {length} exceeds remaining input length {_remaining}"
            )
        outputs = []
        for _ in range(length):
            outputs.append(SCSpecTypeDef.unpack(unpacker, depth_limit - 1))
        return cls(
            doc=doc,
            name=name,
            inputs=inputs,
            outputs=outputs,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCSpecFunctionV0:
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
    def from_xdr(cls, xdr: str) -> SCSpecFunctionV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCSpecFunctionV0:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "doc": String.to_json_dict(self.doc),
            "name": self.name.to_json_dict(),
            "inputs": [item.to_json_dict() for item in self.inputs],
            "outputs": [item.to_json_dict() for item in self.outputs],
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SCSpecFunctionV0:
        doc = String.from_json_dict(json_dict["doc"])
        name = SCSymbol.from_json_dict(json_dict["name"])
        inputs = [
            SCSpecFunctionInputV0.from_json_dict(item) for item in json_dict["inputs"]
        ]
        outputs = [SCSpecTypeDef.from_json_dict(item) for item in json_dict["outputs"]]
        return cls(
            doc=doc,
            name=name,
            inputs=inputs,
            outputs=outputs,
        )

    def __hash__(self):
        return hash(
            (
                self.doc,
                self.name,
                self.inputs,
                self.outputs,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.doc == other.doc
            and self.name == other.name
            and self.inputs == other.inputs
            and self.outputs == other.outputs
        )

    def __repr__(self):
        out = [
            f"doc={self.doc}",
            f"name={self.name}",
            f"inputs={self.inputs}",
            f"outputs={self.outputs}",
        ]
        return f"<SCSpecFunctionV0 [{', '.join(out)}]>"
