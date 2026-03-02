# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, Opaque

__all__ = ["Signature"]


class Signature:
    """
    XDR Source Code::

        typedef opaque Signature<64>;
    """

    def __init__(self, signature: bytes) -> None:
        _expect_max_length = 64
        if signature and len(signature) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `signature` should be {_expect_max_length}, but got {len(signature)}."
            )
        self.signature = signature

    def pack(self, packer: Packer) -> None:
        Opaque(self.signature, 64, False).pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> Signature:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        signature = Opaque.unpack(unpacker, 64, False)
        return cls(signature)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Signature:
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
    def from_xdr(cls, xdr: str) -> Signature:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Signature:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        return Opaque.to_json_dict(self.signature)

    @classmethod
    def from_json_dict(cls, json_value: str) -> Signature:
        return cls(Opaque.from_json_dict(json_value))

    def __hash__(self):
        return hash((self.signature,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.signature == other.signature

    def __repr__(self):
        return f"<Signature [signature={self.signature}]>"
