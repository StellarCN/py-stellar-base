# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .signer_key import SignerKey
from .uint32 import Uint32

__all__ = ["Signer"]


class Signer:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct Signer
    {
        SignerKey key;
        uint32 weight; // really only need 1 byte
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        key: SignerKey,
        weight: Uint32,
    ) -> None:
        self.key = key
        self.weight = weight

    def pack(self, packer: Packer) -> None:
        self.key.pack(packer)
        self.weight.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Signer":
        key = SignerKey.unpack(unpacker)
        weight = Uint32.unpack(unpacker)
        return cls(
            key=key,
            weight=weight,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "Signer":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Signer":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.key == other.key and self.weight == other.weight

    def __str__(self):
        out = [
            f"key={self.key}",
            f"weight={self.weight}",
        ]
        return f"<Signer {[', '.join(out)]}>"
