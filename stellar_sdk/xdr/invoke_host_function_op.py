# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib3 import Packer, Unpacker

from .constants import *
from .host_function import HostFunction

__all__ = ["InvokeHostFunctionOp"]


class InvokeHostFunctionOp:
    """
    XDR Source Code::

        struct InvokeHostFunctionOp
        {
            // The host functions to invoke. The functions will be executed
            // in the same fashion as operations: either all functions will
            // be successfully applied or all fail if at least one of them
            // fails.
            HostFunction functions<MAX_OPS_PER_TX>;
        };
    """

    def __init__(
        self,
        functions: List[HostFunction],
    ) -> None:
        _expect_max_length = MAX_OPS_PER_TX
        if functions and len(functions) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `functions` should be {_expect_max_length}, but got {len(functions)}."
            )
        self.functions = functions

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.functions))
        for functions_item in self.functions:
            functions_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "InvokeHostFunctionOp":
        length = unpacker.unpack_uint()
        functions = []
        for _ in range(length):
            functions.append(HostFunction.unpack(unpacker))
        return cls(
            functions=functions,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "InvokeHostFunctionOp":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "InvokeHostFunctionOp":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.functions == other.functions

    def __str__(self):
        out = [
            f"functions={self.functions}",
        ]
        return f"<InvokeHostFunctionOp [{', '.join(out)}]>"
