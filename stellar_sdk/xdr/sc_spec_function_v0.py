# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import String
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
            SCSpecFunctionInputV0 inputs<10>;
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
        _expect_max_length = 10
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
    def unpack(cls, unpacker: Unpacker) -> SCSpecFunctionV0:
        doc = String.unpack(unpacker)
        name = SCSymbol.unpack(unpacker)
        length = unpacker.unpack_uint()
        inputs = []
        for _ in range(length):
            inputs.append(SCSpecFunctionInputV0.unpack(unpacker))
        length = unpacker.unpack_uint()
        outputs = []
        for _ in range(length):
            outputs.append(SCSpecTypeDef.unpack(unpacker))
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
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCSpecFunctionV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
