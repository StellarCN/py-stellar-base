# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .base import Opaque

__all__ = ["SignatureHint"]


class SignatureHint:
    """
    XDR Source Code::

        typedef opaque SignatureHint[4];
    """

    def __init__(self, signature_hint: bytes) -> None:
        self.signature_hint = signature_hint

    def pack(self, packer: Packer) -> None:
        Opaque(self.signature_hint, 4, True).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SignatureHint:
        signature_hint = Opaque.unpack(unpacker, 4, True)
        return cls(signature_hint)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SignatureHint:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SignatureHint:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(self.signature_hint)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.signature_hint == other.signature_hint

    def __repr__(self):
        return f"<SignatureHint [signature_hint={self.signature_hint}]>"
