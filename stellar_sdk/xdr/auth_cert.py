# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .curve25519_public import Curve25519Public
from .signature import Signature
from .uint64 import Uint64

__all__ = ["AuthCert"]


class AuthCert:
    """
    XDR Source Code::

        struct AuthCert
        {
            Curve25519Public pubkey;
            uint64 expiration;
            Signature sig;
        };
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> AuthCert:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        pubkey = Curve25519Public.unpack(unpacker, depth_limit - 1)
        expiration = Uint64.unpack(unpacker, depth_limit - 1)
        sig = Signature.unpack(unpacker, depth_limit - 1)
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
    def from_xdr_bytes(cls, xdr: bytes) -> AuthCert:
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
    def from_xdr(cls, xdr: str) -> AuthCert:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> AuthCert:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "pubkey": self.pubkey.to_json_dict(),
            "expiration": self.expiration.to_json_dict(),
            "sig": self.sig.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> AuthCert:
        pubkey = Curve25519Public.from_json_dict(json_dict["pubkey"])
        expiration = Uint64.from_json_dict(json_dict["expiration"])
        sig = Signature.from_json_dict(json_dict["sig"])
        return cls(
            pubkey=pubkey,
            expiration=expiration,
            sig=sig,
        )

    def __hash__(self):
        return hash(
            (
                self.pubkey,
                self.expiration,
                self.sig,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.pubkey == other.pubkey
            and self.expiration == other.expiration
            and self.sig == other.sig
        )

    def __repr__(self):
        out = [
            f"pubkey={self.pubkey}",
            f"expiration={self.expiration}",
            f"sig={self.sig}",
        ]
        return f"<AuthCert [{', '.join(out)}]>"
