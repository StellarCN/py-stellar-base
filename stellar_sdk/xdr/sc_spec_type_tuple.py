# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

from .sc_spec_type_def import SCSpecTypeDef

__all__ = ["SCSpecTypeTuple"]


class SCSpecTypeTuple:
    """
    XDR Source Code::

        struct SCSpecTypeTuple
        {
            SCSpecTypeDef valueTypes<12>;
        };
    """

    def __init__(
        self,
        value_types: List[SCSpecTypeDef],
    ) -> None:
        _expect_max_length = 12
        if value_types and len(value_types) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `value_types` should be {_expect_max_length}, but got {len(value_types)}."
            )
        self.value_types = value_types

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.value_types))
        for value_types_item in self.value_types:
            value_types_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCSpecTypeTuple:
        length = unpacker.unpack_uint()
        value_types = []
        for _ in range(length):
            value_types.append(SCSpecTypeDef.unpack(unpacker))
        return cls(
            value_types=value_types,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCSpecTypeTuple:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCSpecTypeTuple:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash((self.value_types,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value_types == other.value_types

    def __repr__(self):
        out = [
            f"value_types={self.value_types}",
        ]
        return f"<SCSpecTypeTuple [{', '.join(out)}]>"
