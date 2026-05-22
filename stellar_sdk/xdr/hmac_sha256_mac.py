# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, Opaque

__all__ = ["HmacSha256Mac"]


class HmacSha256Mac:
    """
    XDR Source Code::

        struct HmacSha256Mac
        {
            opaque mac[32];
        };
    """

    def __init__(
        self,
        mac: bytes,
    ) -> None:
        _expect_length = 32
        if mac and len(mac) != _expect_length:
            raise ValueError(
                f"The length of `mac` should be {_expect_length}, but got {len(mac)}."
            )
        self.mac = mac

    def pack(self, packer: Packer) -> None:
        Opaque(self.mac, 32, True).pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> HmacSha256Mac:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        mac = Opaque.unpack(unpacker, 32, True)
        return cls(
            mac=mac,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> HmacSha256Mac:
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
    def from_xdr(cls, xdr: str) -> HmacSha256Mac:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> HmacSha256Mac:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "mac": Opaque.to_json_dict(self.mac),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> HmacSha256Mac:
        mac = Opaque.from_json_dict(json_dict["mac"])
        return cls(
            mac=mac,
        )

    def __hash__(self):
        return hash((self.mac,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.mac == other.mac

    def __repr__(self):
        out = [
            f"mac={self.mac}",
        ]
        return f"<HmacSha256Mac [{', '.join(out)}]>"
