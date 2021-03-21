# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .curve25519_public import Curve25519Public
from .signature import Signature
from .uint64 import Uint64

__all__ = ["AuthCert"]


class AuthCert:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct AuthCert
    {
        Curve25519Public pubkey;
        uint64 expiration;
        Signature sig;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        pubkey: Curve25519Public,
        expiration: Uint64,
        sig: Signature,
    ) -> None:
        self.pubkey = pubkey
        self.expiration = expiration
        self.sig = sig

    def pack(self, packer: Packer) -> None:
        self.pubkey.pack(packer)
        self.expiration.pack(packer)
        self.sig.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AuthCert":
        pubkey = Curve25519Public.unpack(unpacker)
        expiration = Uint64.unpack(unpacker)
        sig = Signature.unpack(unpacker)
        return cls(
            pubkey=pubkey,
            expiration=expiration,
            sig=sig,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "AuthCert":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AuthCert":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.pubkey == other.pubkey
            and self.expiration == other.expiration
            and self.sig == other.sig
        )

    def __str__(self):
        out = [
            f"pubkey={self.pubkey}",
            f"expiration={self.expiration}",
            f"sig={self.sig}",
        ]
        return f"<AuthCert {[', '.join(out)]}>"
