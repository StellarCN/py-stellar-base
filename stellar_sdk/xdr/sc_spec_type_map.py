# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .sc_spec_type_def import SCSpecTypeDef

__all__ = ["SCSpecTypeMap"]


class SCSpecTypeMap:
    """
    XDR Source Code::

        struct SCSpecTypeMap
        {
            SCSpecTypeDef keyType;
            SCSpecTypeDef valueType;
        };
    """

    def __init__(
        self,
        key_type: SCSpecTypeDef,
        value_type: SCSpecTypeDef,
    ) -> None:
        self.key_type = key_type
        self.value_type = value_type

    def pack(self, packer: Packer) -> None:
        self.key_type.pack(packer)
        self.value_type.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCSpecTypeMap:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        key_type = SCSpecTypeDef.unpack(unpacker, depth_limit - 1)
        value_type = SCSpecTypeDef.unpack(unpacker, depth_limit - 1)
        return cls(
            key_type=key_type,
            value_type=value_type,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCSpecTypeMap:
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
    def from_xdr(cls, xdr: str) -> SCSpecTypeMap:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCSpecTypeMap:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "key_type": self.key_type.to_json_dict(),
            "value_type": self.value_type.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SCSpecTypeMap:
        key_type = SCSpecTypeDef.from_json_dict(json_dict["key_type"])
        value_type = SCSpecTypeDef.from_json_dict(json_dict["value_type"])
        return cls(
            key_type=key_type,
            value_type=value_type,
        )

    def __hash__(self):
        return hash(
            (
                self.key_type,
                self.value_type,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.key_type == other.key_type and self.value_type == other.value_type

    def __repr__(self):
        out = [
            f"key_type={self.key_type}",
            f"value_type={self.value_type}",
        ]
        return f"<SCSpecTypeMap [{', '.join(out)}]>"
