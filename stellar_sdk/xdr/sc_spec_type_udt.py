# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, String

__all__ = ["SCSpecTypeUDT"]


class SCSpecTypeUDT:
    """
    XDR Source Code::

        struct SCSpecTypeUDT
        {
            string name<60>;
        };
    """

    def __init__(
        self,
        name: bytes,
    ) -> None:
        _expect_max_length = 60
        if name and len(name) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `name` should be {_expect_max_length}, but got {len(name)}."
            )
        self.name = name

    def pack(self, packer: Packer) -> None:
        String(self.name, 60).pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCSpecTypeUDT:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        name = String.unpack(unpacker, 60)
        return cls(
            name=name,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCSpecTypeUDT:
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
    def from_xdr(cls, xdr: str) -> SCSpecTypeUDT:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCSpecTypeUDT:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "name": String.to_json_dict(self.name),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SCSpecTypeUDT:
        name = String.from_json_dict(json_dict["name"])
        return cls(
            name=name,
        )

    def __hash__(self):
        return hash((self.name,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.name == other.name

    def __repr__(self):
        out = [
            f"name={self.name}",
        ]
        return f"<SCSpecTypeUDT [{', '.join(out)}]>"
