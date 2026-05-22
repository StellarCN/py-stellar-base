# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .sc_val import SCVal

__all__ = ["SCMapEntry"]


class SCMapEntry:
    """
    XDR Source Code::

        struct SCMapEntry
        {
            SCVal key;
            SCVal val;
        };
    """

    def __init__(
        self,
        key: SCVal,
        val: SCVal,
    ) -> None:
        self.key = key
        self.val = val

    def pack(self, packer: Packer) -> None:
        self.key.pack(packer)
        self.val.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCMapEntry:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        key = SCVal.unpack(unpacker, depth_limit - 1)
        val = SCVal.unpack(unpacker, depth_limit - 1)
        return cls(
            key=key,
            val=val,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCMapEntry:
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
    def from_xdr(cls, xdr: str) -> SCMapEntry:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCMapEntry:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "key": self.key.to_json_dict(),
            "val": self.val.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SCMapEntry:
        key = SCVal.from_json_dict(json_dict["key"])
        val = SCVal.from_json_dict(json_dict["val"])
        return cls(
            key=key,
            val=val,
        )

    def __hash__(self):
        return hash(
            (
                self.key,
                self.val,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.key == other.key and self.val == other.val

    def __repr__(self):
        out = [
            f"key={self.key}",
            f"val={self.val}",
        ]
        return f"<SCMapEntry [{', '.join(out)}]>"
