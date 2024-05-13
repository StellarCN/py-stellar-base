# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .authenticated_message_v0 import AuthenticatedMessageV0
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
        v0: AuthenticatedMessageV0 = None,
    ) -> None:
        self.v = v
        self.v0 = v0

    def pack(self, packer: Packer) -> None:
        self.v.pack(packer)
        if self.v == 0:
            if self.v0 is None:
                raise ValueError("v0 should not be None.")
            self.v0.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> AuthenticatedMessage:
        v = Uint32.unpack(unpacker)
        if v == 0:
            v0 = AuthenticatedMessageV0.unpack(unpacker)
            return cls(v=v, v0=v0)
        return cls(v=v)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> AuthenticatedMessage:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> AuthenticatedMessage:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
        out.append(f"v0={self.v0}") if self.v0 is not None else None
        return f"<AuthenticatedMessage [{', '.join(out)}]>"
