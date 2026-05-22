# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, Opaque

__all__ = ["Uint256"]


class Uint256:
    """
    XDR Source Code::

        typedef opaque uint256[32];
    """

    def __init__(self, uint256: bytes) -> None:
        _expect_length = 32
        if uint256 and len(uint256) != _expect_length:
            raise ValueError(
                f"The length of `uint256` should be {_expect_length}, but got {len(uint256)}."
            )
        self.uint256 = uint256

    def pack(self, packer: Packer) -> None:
        Opaque(self.uint256, 32, True).pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> Uint256:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        uint256 = Opaque.unpack(unpacker, 32, True)
        return cls(uint256)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Uint256:
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
    def from_xdr(cls, xdr: str) -> Uint256:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Uint256:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        return Opaque.to_json_dict(self.uint256)

    @classmethod
    def from_json_dict(cls, json_value: str) -> Uint256:
        return cls(Opaque.from_json_dict(json_value))

    def __hash__(self):
        return hash((self.uint256,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.uint256 == other.uint256

    def __repr__(self):
        return f"<Uint256 [uint256={self.uint256}]>"
