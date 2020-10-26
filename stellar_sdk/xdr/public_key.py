# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .public_key_type import PublicKeyType
from .uint256 import Uint256
from ..exceptions import ValueError

__all__ = ["PublicKey"]


class PublicKey:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union PublicKey switch (PublicKeyType type)
    {
    case PUBLIC_KEY_TYPE_ED25519:
        uint256 ed25519;
    };
    ----------------------------------------------------------------
    """

    def __init__(self, type: PublicKeyType, ed25519: Uint256 = None,) -> None:
        self.type = type
        self.ed25519 = ed25519

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == PublicKeyType.PUBLIC_KEY_TYPE_ED25519:
            if self.ed25519 is None:
                raise ValueError("ed25519 should not be None.")
            self.ed25519.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "PublicKey":
        type = PublicKeyType.unpack(unpacker)
        if type == PublicKeyType.PUBLIC_KEY_TYPE_ED25519:
            ed25519 = Uint256.unpack(unpacker)
            if ed25519 is None:
                raise ValueError("ed25519 should not be None.")
            return cls(type, ed25519=ed25519)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "PublicKey":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "PublicKey":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.type == other.type and self.ed25519 == other.ed25519

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"ed25519={self.ed25519}") if self.ed25519 is not None else None
        return f"<PublicKey {[', '.join(out)]}>"
