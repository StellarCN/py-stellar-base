# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, String

__all__ = ["SCMetaV0"]


class SCMetaV0:
    """
    XDR Source Code::

        struct SCMetaV0
        {
            string key<>;
            string val<>;
        };
    """

    def __init__(
        self,
        key: bytes,
        val: bytes,
    ) -> None:
        _expect_max_length = 4294967295
        if key and len(key) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `key` should be {_expect_max_length}, but got {len(key)}."
            )
        _expect_max_length = 4294967295
        if val and len(val) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `val` should be {_expect_max_length}, but got {len(val)}."
            )
        self.key = key
        self.val = val

    def pack(self, packer: Packer) -> None:
        String(self.key, 4294967295).pack(packer)
        String(self.val, 4294967295).pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCMetaV0:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        key = String.unpack(unpacker, 4294967295)
        val = String.unpack(unpacker, 4294967295)
        return cls(
            key=key,
            val=val,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCMetaV0:
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
    def from_xdr(cls, xdr: str) -> SCMetaV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCMetaV0:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "key": String.to_json_dict(self.key),
            "val": String.to_json_dict(self.val),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SCMetaV0:
        key = String.from_json_dict(json_dict["key"])
        val = String.from_json_dict(json_dict["val"])
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
        return f"<SCMetaV0 [{', '.join(out)}]>"
