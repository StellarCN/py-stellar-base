# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, Opaque
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
        _expect_max_length = 64
        if payload and len(payload) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `payload` should be {_expect_max_length}, but got {len(payload)}."
            )
        self.ed25519 = ed25519
        self.payload = payload

    def pack(self, packer: Packer) -> None:
        self.ed25519.pack(packer)
        Opaque(self.payload, 64, False).pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SignerKeyEd25519SignedPayload:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        ed25519 = Uint256.unpack(unpacker, depth_limit - 1)
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SignerKeyEd25519SignedPayload:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SignerKeyEd25519SignedPayload:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "ed25519": self.ed25519.to_json_dict(),
            "payload": Opaque.to_json_dict(self.payload),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SignerKeyEd25519SignedPayload:
        ed25519 = Uint256.from_json_dict(json_dict["ed25519"])
        payload = Opaque.from_json_dict(json_dict["payload"])
        return cls(
            ed25519=ed25519,
            payload=payload,
        )

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
