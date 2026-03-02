# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .int64 import Int64

__all__ = ["SCNonceKey"]


class SCNonceKey:
    """
    XDR Source Code::

        struct SCNonceKey {
            int64 nonce;
        };
    """

    def __init__(
        self,
        nonce: Int64,
    ) -> None:
        self.nonce = nonce

    def pack(self, packer: Packer) -> None:
        self.nonce.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCNonceKey:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        nonce = Int64.unpack(unpacker, depth_limit - 1)
        return cls(
            nonce=nonce,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCNonceKey:
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
    def from_xdr(cls, xdr: str) -> SCNonceKey:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCNonceKey:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "nonce": self.nonce.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SCNonceKey:
        nonce = Int64.from_json_dict(json_dict["nonce"])
        return cls(
            nonce=nonce,
        )

    def __hash__(self):
        return hash((self.nonce,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.nonce == other.nonce

    def __repr__(self):
        out = [
            f"nonce={self.nonce}",
        ]
        return f"<SCNonceKey [{', '.join(out)}]>"
