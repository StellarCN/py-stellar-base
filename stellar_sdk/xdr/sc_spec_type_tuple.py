# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCSpecTypeTuple:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"value_types length {length} exceeds remaining input length {_remaining}"
            )
        value_types = []
        for _ in range(length):
            value_types.append(SCSpecTypeDef.unpack(unpacker, depth_limit - 1))
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCSpecTypeTuple:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCSpecTypeTuple:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "value_types": [item.to_json_dict() for item in self.value_types],
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SCSpecTypeTuple:
        value_types = [
            SCSpecTypeDef.from_json_dict(item) for item in json_dict["value_types"]
        ]
        return cls(
            value_types=value_types,
        )

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
