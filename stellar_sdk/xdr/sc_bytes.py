# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, Opaque

__all__ = ["SCBytes"]


class SCBytes:
    """
    XDR Source Code::

        typedef opaque SCBytes<>;
    """

    def __init__(self, sc_bytes: bytes) -> None:
        _expect_max_length = 4294967295
        if sc_bytes and len(sc_bytes) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `sc_bytes` should be {_expect_max_length}, but got {len(sc_bytes)}."
            )
        self.sc_bytes = sc_bytes

    def pack(self, packer: Packer) -> None:
        Opaque(self.sc_bytes, 4294967295, False).pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCBytes:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        sc_bytes = Opaque.unpack(unpacker, 4294967295, False)
        return cls(sc_bytes)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCBytes:
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
    def from_xdr(cls, xdr: str) -> SCBytes:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCBytes:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        return Opaque.to_json_dict(self.sc_bytes)

    @classmethod
    def from_json_dict(cls, json_value: str) -> SCBytes:
        return cls(Opaque.from_json_dict(json_value))

    def __hash__(self):
        return hash((self.sc_bytes,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.sc_bytes == other.sc_bytes

    def __repr__(self):
        return f"<SCBytes [sc_bytes={self.sc_bytes}]>"
