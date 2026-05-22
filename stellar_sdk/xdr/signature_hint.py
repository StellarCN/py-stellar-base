# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, Opaque

__all__ = ["SignatureHint"]


class SignatureHint:
    """
    XDR Source Code::

        typedef opaque SignatureHint[4];
    """

    def __init__(self, signature_hint: bytes) -> None:
        _expect_length = 4
        if signature_hint and len(signature_hint) != _expect_length:
            raise ValueError(
                f"The length of `signature_hint` should be {_expect_length}, but got {len(signature_hint)}."
            )
        self.signature_hint = signature_hint

    def pack(self, packer: Packer) -> None:
        Opaque(self.signature_hint, 4, True).pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SignatureHint:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        signature_hint = Opaque.unpack(unpacker, 4, True)
        return cls(signature_hint)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SignatureHint:
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
    def from_xdr(cls, xdr: str) -> SignatureHint:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SignatureHint:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        return Opaque.to_json_dict(self.signature_hint)

    @classmethod
    def from_json_dict(cls, json_value: str) -> SignatureHint:
        return cls(Opaque.from_json_dict(json_value))

    def __hash__(self):
        return hash((self.signature_hint,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.signature_hint == other.signature_hint

    def __repr__(self):
        return f"<SignatureHint [signature_hint={self.signature_hint}]>"
