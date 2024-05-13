# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .base import Opaque
from .uint256 import Uint256

__all__ = ["SignerKeyEd25519SignedPayload"]


class SignerKeyEd25519SignedPayload:
    """
    XDR Source Code::

        struct
            {
                /* Public key that must sign the payload. */
                uint256 ed25519;
                /* Payload to be raw signed by ed25519. */
                opaque payload<64>;
            }
    """

    def __init__(
        self,
        ed25519: Uint256,
        payload: bytes,
    ) -> None:
        self.ed25519 = ed25519
        self.payload = payload

    def pack(self, packer: Packer) -> None:
        self.ed25519.pack(packer)
        Opaque(self.payload, 64, False).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SignerKeyEd25519SignedPayload:
        ed25519 = Uint256.unpack(unpacker)
        payload = Opaque.unpack(unpacker, 64, False)
        return cls(
            ed25519=ed25519,
            payload=payload,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SignerKeyEd25519SignedPayload:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SignerKeyEd25519SignedPayload:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.ed25519,
                self.payload,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.ed25519 == other.ed25519 and self.payload == other.payload

    def __repr__(self):
        out = [
            f"ed25519={self.ed25519}",
            f"payload={self.payload}",
        ]
        return f"<SignerKeyEd25519SignedPayload [{', '.join(out)}]>"
