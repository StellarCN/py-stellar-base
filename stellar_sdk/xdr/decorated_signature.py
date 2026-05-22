# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .signature import Signature
from .signature_hint import SignatureHint

__all__ = ["DecoratedSignature"]


class DecoratedSignature:
    """
    XDR Source Code::

        struct DecoratedSignature
        {
            SignatureHint hint;  // last 4 bytes of the public key, used as a hint
            Signature signature; // actual signature
        };
    """

    def __init__(
        self,
        hint: SignatureHint,
        signature: Signature,
    ) -> None:
        self.hint = hint
        self.signature = signature

    def pack(self, packer: Packer) -> None:
        self.hint.pack(packer)
        self.signature.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> DecoratedSignature:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        hint = SignatureHint.unpack(unpacker, depth_limit - 1)
        signature = Signature.unpack(unpacker, depth_limit - 1)
        return cls(
            hint=hint,
            signature=signature,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> DecoratedSignature:
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
    def from_xdr(cls, xdr: str) -> DecoratedSignature:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> DecoratedSignature:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "hint": self.hint.to_json_dict(),
            "signature": self.signature.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> DecoratedSignature:
        hint = SignatureHint.from_json_dict(json_dict["hint"])
        signature = Signature.from_json_dict(json_dict["signature"])
        return cls(
            hint=hint,
            signature=signature,
        )

    def __hash__(self):
        return hash(
            (
                self.hint,
                self.signature,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.hint == other.hint and self.signature == other.signature

    def __repr__(self):
        out = [
            f"hint={self.hint}",
            f"signature={self.signature}",
        ]
        return f"<DecoratedSignature [{', '.join(out)}]>"
