# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .host_function import HostFunction
from .soroban_authorization_entry import SorobanAuthorizationEntry

__all__ = ["InvokeHostFunctionOp"]


class InvokeHostFunctionOp:
    """
    XDR Source Code::

        struct InvokeHostFunctionOp
        {
            // Host function to invoke.
            HostFunction hostFunction;
            // Per-address authorizations for this host function.
            SorobanAuthorizationEntry auth<>;
        };
    """

    def __init__(
        self,
        host_function: HostFunction,
        auth: List[SorobanAuthorizationEntry],
    ) -> None:
        _expect_max_length = 4294967295
        if auth and len(auth) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `auth` should be {_expect_max_length}, but got {len(auth)}."
            )
        self.host_function = host_function
        self.auth = auth

    def pack(self, packer: Packer) -> None:
        self.host_function.pack(packer)
        packer.pack_uint(len(self.auth))
        for auth_item in self.auth:
            auth_item.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> InvokeHostFunctionOp:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        host_function = HostFunction.unpack(unpacker, depth_limit - 1)
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"auth length {length} exceeds remaining input length {_remaining}"
            )
        auth = []
        for _ in range(length):
            auth.append(SorobanAuthorizationEntry.unpack(unpacker, depth_limit - 1))
        return cls(
            host_function=host_function,
            auth=auth,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> InvokeHostFunctionOp:
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
    def from_xdr(cls, xdr: str) -> InvokeHostFunctionOp:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> InvokeHostFunctionOp:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "host_function": self.host_function.to_json_dict(),
            "auth": [item.to_json_dict() for item in self.auth],
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> InvokeHostFunctionOp:
        host_function = HostFunction.from_json_dict(json_dict["host_function"])
        auth = [
            SorobanAuthorizationEntry.from_json_dict(item) for item in json_dict["auth"]
        ]
        return cls(
            host_function=host_function,
            auth=auth,
        )

    def __hash__(self):
        return hash(
            (
                self.host_function,
                self.auth,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.host_function == other.host_function and self.auth == other.auth

    def __repr__(self):
        out = [
            f"host_function={self.host_function}",
            f"auth={self.auth}",
        ]
        return f"<InvokeHostFunctionOp [{', '.join(out)}]>"
