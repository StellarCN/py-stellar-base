# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .soroban_authorized_function import SorobanAuthorizedFunction

__all__ = ["SorobanAuthorizedInvocation"]


class SorobanAuthorizedInvocation:
    """
    XDR Source Code::

        struct SorobanAuthorizedInvocation
        {
            SorobanAuthorizedFunction function;
            SorobanAuthorizedInvocation subInvocations<>;
        };
    """

    def __init__(
        self,
        function: SorobanAuthorizedFunction,
        sub_invocations: List["SorobanAuthorizedInvocation"],
    ) -> None:
        _expect_max_length = 4294967295
        if sub_invocations and len(sub_invocations) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `sub_invocations` should be {_expect_max_length}, but got {len(sub_invocations)}."
            )
        self.function = function
        self.sub_invocations = sub_invocations

    def pack(self, packer: Packer) -> None:
        self.function.pack(packer)
        packer.pack_uint(len(self.sub_invocations))
        for sub_invocations_item in self.sub_invocations:
            sub_invocations_item.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SorobanAuthorizedInvocation:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        function = SorobanAuthorizedFunction.unpack(unpacker, depth_limit - 1)
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"sub_invocations length {length} exceeds remaining input length {_remaining}"
            )
        sub_invocations = []
        for _ in range(length):
            sub_invocations.append(
                SorobanAuthorizedInvocation.unpack(unpacker, depth_limit - 1)
            )
        return cls(
            function=function,
            sub_invocations=sub_invocations,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SorobanAuthorizedInvocation:
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
    def from_xdr(cls, xdr: str) -> SorobanAuthorizedInvocation:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SorobanAuthorizedInvocation:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "function": self.function.to_json_dict(),
            "sub_invocations": [item.to_json_dict() for item in self.sub_invocations],
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SorobanAuthorizedInvocation:
        function = SorobanAuthorizedFunction.from_json_dict(json_dict["function"])
        sub_invocations = [
            SorobanAuthorizedInvocation.from_json_dict(item)
            for item in json_dict["sub_invocations"]
        ]
        return cls(
            function=function,
            sub_invocations=sub_invocations,
        )

    def __hash__(self):
        return hash(
            (
                self.function,
                self.sub_invocations,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.function == other.function
            and self.sub_invocations == other.sub_invocations
        )

    def __repr__(self):
        out = [
            f"function={self.function}",
            f"sub_invocations={self.sub_invocations}",
        ]
        return f"<SorobanAuthorizedInvocation [{', '.join(out)}]>"
