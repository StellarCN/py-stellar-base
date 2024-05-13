# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .soroban_authorized_invocation import SorobanAuthorizedInvocation
from .soroban_credentials import SorobanCredentials

__all__ = ["SorobanAuthorizationEntry"]


class SorobanAuthorizationEntry:
    """
    XDR Source Code::

        struct SorobanAuthorizationEntry
        {
            SorobanCredentials credentials;
            SorobanAuthorizedInvocation rootInvocation;
        };
    """

    def __init__(
        self,
        credentials: SorobanCredentials,
        root_invocation: SorobanAuthorizedInvocation,
    ) -> None:
        self.credentials = credentials
        self.root_invocation = root_invocation

    def pack(self, packer: Packer) -> None:
        self.credentials.pack(packer)
        self.root_invocation.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SorobanAuthorizationEntry:
        credentials = SorobanCredentials.unpack(unpacker)
        root_invocation = SorobanAuthorizedInvocation.unpack(unpacker)
        return cls(
            credentials=credentials,
            root_invocation=root_invocation,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SorobanAuthorizationEntry:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SorobanAuthorizationEntry:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.credentials,
                self.root_invocation,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.credentials == other.credentials
            and self.root_invocation == other.root_invocation
        )

    def __repr__(self):
        out = [
            f"credentials={self.credentials}",
            f"root_invocation={self.root_invocation}",
        ]
        return f"<SorobanAuthorizationEntry [{', '.join(out)}]>"
