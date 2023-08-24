# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .sc_address import SCAddress
from .sc_symbol import SCSymbol
from .sc_vec import SCVec

__all__ = ["SorobanAuthorizedContractFunction"]


class SorobanAuthorizedContractFunction:
    """
    XDR Source Code::

        struct SorobanAuthorizedContractFunction
        {
            SCAddress contractAddress;
            SCSymbol functionName;
            SCVec args;
        };
    """

    def __init__(
        self,
        contract_address: SCAddress,
        function_name: SCSymbol,
        args: SCVec,
    ) -> None:
        self.contract_address = contract_address
        self.function_name = function_name
        self.args = args

    def pack(self, packer: Packer) -> None:
        self.contract_address.pack(packer)
        self.function_name.pack(packer)
        self.args.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SorobanAuthorizedContractFunction:
        contract_address = SCAddress.unpack(unpacker)
        function_name = SCSymbol.unpack(unpacker)
        args = SCVec.unpack(unpacker)
        return cls(
            contract_address=contract_address,
            function_name=function_name,
            args=args,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SorobanAuthorizedContractFunction:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SorobanAuthorizedContractFunction:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.contract_address,
                self.function_name,
                self.args,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.contract_address == other.contract_address
            and self.function_name == other.function_name
            and self.args == other.args
        )

    def __str__(self):
        out = [
            f"contract_address={self.contract_address}",
            f"function_name={self.function_name}",
            f"args={self.args}",
        ]
        return f"<SorobanAuthorizedContractFunction [{', '.join(out)}]>"
