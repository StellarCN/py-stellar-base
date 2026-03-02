# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .authenticated_message_v0 import AuthenticatedMessageV0
from .base import DEFAULT_XDR_MAX_DEPTH
from .uint32 import Uint32

__all__ = ["AuthenticatedMessage"]


class AuthenticatedMessage:
    """
    XDR Source Code::

        union AuthenticatedMessage switch (uint32 v)
        {
        case 0:
            struct
            {
                uint64 sequence;
                StellarMessage message;
                HmacSha256Mac mac;
            } v0;
        };
    """

    def __init__(
        self,
        v: Uint32,
        v0: Optional[AuthenticatedMessageV0] = None,
    ) -> None:
        self.v = v
        self.v0 = v0

    def pack(self, packer: Packer) -> None:
        self.v.pack(packer)
        if self.v.uint32 == 0:
            if self.v0 is None:
                raise ValueError("v0 should not be None.")
            self.v0.pack(packer)
            return
        raise ValueError("Invalid v.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> AuthenticatedMessage:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        v = Uint32.unpack(unpacker)
        if v.uint32 == 0:
            v0 = AuthenticatedMessageV0.unpack(unpacker, depth_limit - 1)
            return cls(v=v, v0=v0)
        raise ValueError("Invalid v.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> AuthenticatedMessage:
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
    def from_xdr(cls, xdr: str) -> AuthenticatedMessage:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> AuthenticatedMessage:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.v.uint32 == 0:
            assert self.v0 is not None
            return {"v0": self.v0.to_json_dict()}
        raise ValueError(f"Unknown v in AuthenticatedMessage: {self.v}")

    @classmethod
    def from_json_dict(cls, json_value: dict) -> AuthenticatedMessage:
        if len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for AuthenticatedMessage, got: {json_value}"
            )
        key = next(iter(json_value))
        v = Uint32(int(key[1:]))
        if key == "v0":
            v0 = AuthenticatedMessageV0.from_json_dict(json_value["v0"])
            return cls(v=v, v0=v0)
        raise ValueError(f"Unknown key '{key}' for AuthenticatedMessage")

    def __hash__(self):
        return hash(
            (
                self.v,
                self.v0,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v and self.v0 == other.v0

    def __repr__(self):
        out = []
        out.append(f"v={self.v}")
        if self.v0 is not None:
            out.append(f"v0={self.v0}")
        return f"<AuthenticatedMessage [{', '.join(out)}]>"
