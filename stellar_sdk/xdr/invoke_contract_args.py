# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

from .sc_address import SCAddress
from .sc_symbol import SCSymbol
from .sc_val import SCVal

__all__ = ["InvokeContractArgs"]


class InvokeContractArgs:
    """
    XDR Source Code::

        struct InvokeContractArgs {
            SCAddress contractAddress;
            SCSymbol functionName;
            SCVal args<>;
        };
    """

    def __init__(
        self,
        contract_address: SCAddress,
        function_name: SCSymbol,
        args: List[SCVal],
    ) -> None:
        _expect_max_length = 4294967295
        if args and len(args) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `args` should be {_expect_max_length}, but got {len(args)}."
            )
        self.contract_address = contract_address
        self.function_name = function_name
        self.args = args

    def pack(self, packer: Packer) -> None:
        self.contract_address.pack(packer)
        self.function_name.pack(packer)
        packer.pack_uint(len(self.args))
        for args_item in self.args:
            args_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> InvokeContractArgs:
        contract_address = SCAddress.unpack(unpacker)
        function_name = SCSymbol.unpack(unpacker)
        length = unpacker.unpack_uint()
        args = []
        for _ in range(length):
            args.append(SCVal.unpack(unpacker))
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
    def from_xdr_bytes(cls, xdr: bytes) -> InvokeContractArgs:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> InvokeContractArgs:
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

    def __repr__(self):
        out = [
            f"contract_address={self.contract_address}",
            f"function_name={self.function_name}",
            f"args={self.args}",
        ]
        return f"<InvokeContractArgs [{', '.join(out)}]>"
