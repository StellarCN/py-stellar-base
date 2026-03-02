# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, Integer

__all__ = ["Auth"]


class Auth:
    """
    XDR Source Code::

        struct Auth
        {
            int flags;
        };
    """

    def __init__(
        self,
        flags: int,
    ) -> None:
        self.flags = flags

    def pack(self, packer: Packer) -> None:
        Integer(self.flags).pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> Auth:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        flags = Integer.unpack(unpacker)
        return cls(
            flags=flags,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Auth:
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
    def from_xdr(cls, xdr: str) -> Auth:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Auth:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "flags": Integer.to_json_dict(self.flags),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> Auth:
        flags = Integer.from_json_dict(json_dict["flags"])
        return cls(
            flags=flags,
        )

    def __hash__(self):
        return hash((self.flags,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.flags == other.flags

    def __repr__(self):
        out = [
            f"flags={self.flags}",
        ]
        return f"<Auth [{', '.join(out)}]>"
