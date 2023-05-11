# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib3 import Packer, Unpacker

from .signature import Signature
from .uint256 import Uint256

__all__ = ["ContractIDFromEd25519PublicKey"]


class ContractIDFromEd25519PublicKey:
    """
    XDR Source Code::

        struct
            {
                uint256 key;
                Signature signature;
                uint256 salt;
            }
    """

    def __init__(
        self,
        key: Uint256,
        signature: Signature,
        salt: Uint256,
    ) -> None:
        self.key = key
        self.signature = signature
        self.salt = salt

    def pack(self, packer: Packer) -> None:
        self.key.pack(packer)
        self.signature.pack(packer)
        self.salt.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ContractIDFromEd25519PublicKey":
        key = Uint256.unpack(unpacker)
        signature = Signature.unpack(unpacker)
        salt = Uint256.unpack(unpacker)
        return cls(
            key=key,
            signature=signature,
            salt=salt,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "ContractIDFromEd25519PublicKey":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ContractIDFromEd25519PublicKey":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.key == other.key
            and self.signature == other.signature
            and self.salt == other.salt
        )

    def __str__(self):
        out = [
            f"key={self.key}",
            f"signature={self.signature}",
            f"salt={self.salt}",
        ]
        return f"<ContractIDFromEd25519PublicKey [{', '.join(out)}]>"
