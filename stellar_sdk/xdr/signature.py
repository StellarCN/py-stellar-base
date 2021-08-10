# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .base import Opaque

__all__ = ["Signature"]


class Signature:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef opaque Signature<64>;
    ----------------------------------------------------------------
    """

    def __init__(self, signature: bytes) -> None:
        self.signature = signature

    def pack(self, packer: Packer) -> None:
        Opaque(self.signature, 64, False).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Signature":
        signature = Opaque.unpack(unpacker, 64, False)
        return cls(signature)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "Signature":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Signature":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.signature == other.signature

    def __str__(self):
        return f"<Signature [signature={self.signature}]>"
