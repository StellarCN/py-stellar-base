# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib import Packer, Unpacker

from .sc_spec_type_def import SCSpecTypeDef
from .sc_symbol import SCSymbol

__all__ = ["SCSpecFunctionV0"]


class SCSpecFunctionV0:
    """
    XDR Source Code::

        struct SCSpecFunctionV0
        {
            SCSymbol name;
            SCSpecTypeDef inputTypes<10>;
            SCSpecTypeDef outputTypes<1>;
        };
    """

    def __init__(
        self,
        name: SCSymbol,
        input_types: List[SCSpecTypeDef],
        output_types: List[SCSpecTypeDef],
    ) -> None:
        _expect_max_length = 10
        if input_types and len(input_types) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `input_types` should be {_expect_max_length}, but got {len(input_types)}."
            )
        _expect_max_length = 1
        if output_types and len(output_types) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `output_types` should be {_expect_max_length}, but got {len(output_types)}."
            )
        self.name = name
        self.input_types = input_types
        self.output_types = output_types

    def pack(self, packer: Packer) -> None:
        self.name.pack(packer)
        packer.pack_uint(len(self.input_types))
        for input_types_item in self.input_types:
            input_types_item.pack(packer)
        packer.pack_uint(len(self.output_types))
        for output_types_item in self.output_types:
            output_types_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCSpecFunctionV0":
        name = SCSymbol.unpack(unpacker)
        length = unpacker.unpack_uint()
        input_types = []
        for _ in range(length):
            input_types.append(SCSpecTypeDef.unpack(unpacker))
        length = unpacker.unpack_uint()
        output_types = []
        for _ in range(length):
            output_types.append(SCSpecTypeDef.unpack(unpacker))
        return cls(
            name=name,
            input_types=input_types,
            output_types=output_types,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCSpecFunctionV0":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCSpecFunctionV0":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.name == other.name
            and self.input_types == other.input_types
            and self.output_types == other.output_types
        )

    def __str__(self):
        out = [
            f"name={self.name}",
            f"input_types={self.input_types}",
            f"output_types={self.output_types}",
        ]
        return f"<SCSpecFunctionV0 [{', '.join(out)}]>"
