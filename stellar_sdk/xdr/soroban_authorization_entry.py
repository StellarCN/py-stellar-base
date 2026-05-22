# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SorobanAuthorizationEntry:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        credentials = SorobanCredentials.unpack(unpacker, depth_limit - 1)
        root_invocation = SorobanAuthorizedInvocation.unpack(unpacker, depth_limit - 1)
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SorobanAuthorizationEntry:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SorobanAuthorizationEntry:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "credentials": self.credentials.to_json_dict(),
            "root_invocation": self.root_invocation.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SorobanAuthorizationEntry:
        credentials = SorobanCredentials.from_json_dict(json_dict["credentials"])
        root_invocation = SorobanAuthorizedInvocation.from_json_dict(
            json_dict["root_invocation"]
        )
        return cls(
            credentials=credentials,
            root_invocation=root_invocation,
        )

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
