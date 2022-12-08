# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .host_function import HostFunction
from .ledger_footprint import LedgerFootprint

__all__ = ["InvokeHostFunctionOp"]


class InvokeHostFunctionOp:
    """
    XDR Source Code::

        struct InvokeHostFunctionOp
        {
            // The host function to invoke
            HostFunction function;
            // The footprint for this invocation
            LedgerFootprint footprint;
        };
    """

    def __init__(
        self,
        function: HostFunction,
        footprint: LedgerFootprint,
    ) -> None:
        self.function = function
        self.footprint = footprint

    def pack(self, packer: Packer) -> None:
        self.function.pack(packer)
        self.footprint.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "InvokeHostFunctionOp":
        function = HostFunction.unpack(unpacker)
        footprint = LedgerFootprint.unpack(unpacker)
        return cls(
            function=function,
            footprint=footprint,
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
        return self.function == other.function and self.footprint == other.footprint

    def __str__(self):
        out = [
            f"function={self.function}",
            f"footprint={self.footprint}",
        ]
        return f"<InvokeHostFunctionOp [{', '.join(out)}]>"
