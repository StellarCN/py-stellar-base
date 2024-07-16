# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .base import Opaque
from .create_contract_args import CreateContractArgs
from .host_function_type import HostFunctionType
from .invoke_contract_args import InvokeContractArgs

__all__ = ["HostFunction"]


class HostFunction:
    """
    XDR Source Code::

        union HostFunction switch (HostFunctionType type)
        {
        case HOST_FUNCTION_TYPE_INVOKE_CONTRACT:
            InvokeContractArgs invokeContract;
        case HOST_FUNCTION_TYPE_CREATE_CONTRACT:
            CreateContractArgs createContract;
        case HOST_FUNCTION_TYPE_UPLOAD_CONTRACT_WASM:
            opaque wasm<>;
        };
    """

    def __init__(
        self,
        type: HostFunctionType,
        invoke_contract: InvokeContractArgs = None,
        create_contract: CreateContractArgs = None,
        wasm: bytes = None,
    ) -> None:
        self.type = type
        self.invoke_contract = invoke_contract
        self.create_contract = create_contract
        self.wasm = wasm

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == HostFunctionType.HOST_FUNCTION_TYPE_INVOKE_CONTRACT:
            if self.invoke_contract is None:
                raise ValueError("invoke_contract should not be None.")
            self.invoke_contract.pack(packer)
            return
        if self.type == HostFunctionType.HOST_FUNCTION_TYPE_CREATE_CONTRACT:
            if self.create_contract is None:
                raise ValueError("create_contract should not be None.")
            self.create_contract.pack(packer)
            return
        if self.type == HostFunctionType.HOST_FUNCTION_TYPE_UPLOAD_CONTRACT_WASM:
            if self.wasm is None:
                raise ValueError("wasm should not be None.")
            Opaque(self.wasm, 4294967295, False).pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> HostFunction:
        type = HostFunctionType.unpack(unpacker)
        if type == HostFunctionType.HOST_FUNCTION_TYPE_INVOKE_CONTRACT:
            invoke_contract = InvokeContractArgs.unpack(unpacker)
            return cls(type=type, invoke_contract=invoke_contract)
        if type == HostFunctionType.HOST_FUNCTION_TYPE_CREATE_CONTRACT:
            create_contract = CreateContractArgs.unpack(unpacker)
            return cls(type=type, create_contract=create_contract)
        if type == HostFunctionType.HOST_FUNCTION_TYPE_UPLOAD_CONTRACT_WASM:
            wasm = Opaque.unpack(unpacker, 4294967295, False)
            return cls(type=type, wasm=wasm)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> HostFunction:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> HostFunction:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.type,
                self.invoke_contract,
                self.create_contract,
                self.wasm,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.invoke_contract == other.invoke_contract
            and self.create_contract == other.create_contract
            and self.wasm == other.wasm
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        (
            out.append(f"invoke_contract={self.invoke_contract}")
            if self.invoke_contract is not None
            else None
        )
        (
            out.append(f"create_contract={self.create_contract}")
            if self.create_contract is not None
            else None
        )
        out.append(f"wasm={self.wasm}") if self.wasm is not None else None
        return f"<HostFunction [{', '.join(out)}]>"
