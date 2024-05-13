# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

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
    def unpack(cls, unpacker: Unpacker) -> SorobanAuthorizedInvocation:
        function = SorobanAuthorizedFunction.unpack(unpacker)
        length = unpacker.unpack_uint()
        sub_invocations = []
        for _ in range(length):
            sub_invocations.append(SorobanAuthorizedInvocation.unpack(unpacker))
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
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SorobanAuthorizedInvocation:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
