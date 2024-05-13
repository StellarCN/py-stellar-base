# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

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
    def unpack(cls, unpacker: Unpacker) -> DecoratedSignature:
        hint = SignatureHint.unpack(unpacker)
        signature = Signature.unpack(unpacker)
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
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> DecoratedSignature:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
