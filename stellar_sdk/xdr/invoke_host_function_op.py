# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib import Packer, Unpacker

from .contract_auth import ContractAuth
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
            // Per-address authorizations for this host fn
            // Currently only supported for INVOKE_CONTRACT function
            ContractAuth auth<>;
        };
    """

    def __init__(
        self,
        function: HostFunction,
        footprint: LedgerFootprint,
        auth: List[ContractAuth],
    ) -> None:
        _expect_max_length = 4294967295
        if auth and len(auth) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `auth` should be {_expect_max_length}, but got {len(auth)}."
            )
        self.function = function
        self.footprint = footprint
        self.auth = auth

    def pack(self, packer: Packer) -> None:
        self.function.pack(packer)
        self.footprint.pack(packer)
        packer.pack_uint(len(self.auth))
        for auth_item in self.auth:
            auth_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "InvokeHostFunctionOp":
        function = HostFunction.unpack(unpacker)
        footprint = LedgerFootprint.unpack(unpacker)
        length = unpacker.unpack_uint()
        auth = []
        for _ in range(length):
            auth.append(ContractAuth.unpack(unpacker))
        return cls(
            function=function,
            footprint=footprint,
            auth=auth,
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
        return (
            self.function == other.function
            and self.footprint == other.footprint
            and self.auth == other.auth
        )

    def __str__(self):
        out = [
            f"function={self.function}",
            f"footprint={self.footprint}",
            f"auth={self.auth}",
        ]
        return f"<InvokeHostFunctionOp [{', '.join(out)}]>"
