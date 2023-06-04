# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib3 import Packer, Unpacker

from .create_contract_args import CreateContractArgs
from .host_function_type import HostFunctionType
from .sc_vec import SCVec
from .upload_contract_wasm_args import UploadContractWasmArgs

__all__ = ["HostFunctionArgs"]


class HostFunctionArgs:
    """
    XDR Source Code::

        union HostFunctionArgs switch (HostFunctionType type)
        {
        case HOST_FUNCTION_TYPE_INVOKE_CONTRACT:
            SCVec invokeContract;
        case HOST_FUNCTION_TYPE_CREATE_CONTRACT:
            CreateContractArgs createContract;
        case HOST_FUNCTION_TYPE_UPLOAD_CONTRACT_WASM:
            UploadContractWasmArgs uploadContractWasm;
        };
    """

    def __init__(
        self,
        type: HostFunctionType,
        invoke_contract: SCVec = None,
        create_contract: CreateContractArgs = None,
        upload_contract_wasm: UploadContractWasmArgs = None,
    ) -> None:
        self.type = type
        self.invoke_contract = invoke_contract
        self.create_contract = create_contract
        self.upload_contract_wasm = upload_contract_wasm

    @classmethod
    def from_host_function_type_invoke_contract(
        cls, invoke_contract: SCVec
    ) -> "HostFunctionArgs":
        return cls(
            HostFunctionType.HOST_FUNCTION_TYPE_INVOKE_CONTRACT,
            invoke_contract=invoke_contract,
        )

    @classmethod
    def from_host_function_type_create_contract(
        cls, create_contract: CreateContractArgs
    ) -> "HostFunctionArgs":
        return cls(
            HostFunctionType.HOST_FUNCTION_TYPE_CREATE_CONTRACT,
            create_contract=create_contract,
        )

    @classmethod
    def from_host_function_type_upload_contract_wasm(
        cls, upload_contract_wasm: UploadContractWasmArgs
    ) -> "HostFunctionArgs":
        return cls(
            HostFunctionType.HOST_FUNCTION_TYPE_UPLOAD_CONTRACT_WASM,
            upload_contract_wasm=upload_contract_wasm,
        )

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
            if self.upload_contract_wasm is None:
                raise ValueError("upload_contract_wasm should not be None.")
            self.upload_contract_wasm.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "HostFunctionArgs":
        type = HostFunctionType.unpack(unpacker)
        if type == HostFunctionType.HOST_FUNCTION_TYPE_INVOKE_CONTRACT:
            invoke_contract = SCVec.unpack(unpacker)
            return cls(type=type, invoke_contract=invoke_contract)
        if type == HostFunctionType.HOST_FUNCTION_TYPE_CREATE_CONTRACT:
            create_contract = CreateContractArgs.unpack(unpacker)
            return cls(type=type, create_contract=create_contract)
        if type == HostFunctionType.HOST_FUNCTION_TYPE_UPLOAD_CONTRACT_WASM:
            upload_contract_wasm = UploadContractWasmArgs.unpack(unpacker)
            return cls(type=type, upload_contract_wasm=upload_contract_wasm)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "HostFunctionArgs":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "HostFunctionArgs":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.invoke_contract == other.invoke_contract
            and self.create_contract == other.create_contract
            and self.upload_contract_wasm == other.upload_contract_wasm
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(
            f"invoke_contract={self.invoke_contract}"
        ) if self.invoke_contract is not None else None
        out.append(
            f"create_contract={self.create_contract}"
        ) if self.create_contract is not None else None
        out.append(
            f"upload_contract_wasm={self.upload_contract_wasm}"
        ) if self.upload_contract_wasm is not None else None
        return f"<HostFunctionArgs [{', '.join(out)}]>"
