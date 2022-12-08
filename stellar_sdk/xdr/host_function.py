# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .create_contract_args import CreateContractArgs
from .host_function_type import HostFunctionType
from .install_contract_code_args import InstallContractCodeArgs
from .sc_vec import SCVec

__all__ = ["HostFunction"]


class HostFunction:
    """
    XDR Source Code::

        union HostFunction switch (HostFunctionType type)
        {
        case HOST_FUNCTION_TYPE_INVOKE_CONTRACT:
            SCVec invokeArgs;
        case HOST_FUNCTION_TYPE_CREATE_CONTRACT:
            CreateContractArgs createContractArgs;
        case HOST_FUNCTION_TYPE_INSTALL_CONTRACT_CODE:
            InstallContractCodeArgs installContractCodeArgs;
        };
    """

    def __init__(
        self,
        type: HostFunctionType,
        invoke_args: SCVec = None,
        create_contract_args: CreateContractArgs = None,
        install_contract_code_args: InstallContractCodeArgs = None,
    ) -> None:
        self.type = type
        self.invoke_args = invoke_args
        self.create_contract_args = create_contract_args
        self.install_contract_code_args = install_contract_code_args

    @classmethod
    def from_host_function_type_invoke_contract(
        cls, invoke_args: SCVec
    ) -> "HostFunction":
        return cls(
            HostFunctionType.HOST_FUNCTION_TYPE_INVOKE_CONTRACT, invoke_args=invoke_args
        )

    @classmethod
    def from_host_function_type_create_contract(
        cls, create_contract_args: CreateContractArgs
    ) -> "HostFunction":
        return cls(
            HostFunctionType.HOST_FUNCTION_TYPE_CREATE_CONTRACT,
            create_contract_args=create_contract_args,
        )

    @classmethod
    def from_host_function_type_install_contract_code(
        cls, install_contract_code_args: InstallContractCodeArgs
    ) -> "HostFunction":
        return cls(
            HostFunctionType.HOST_FUNCTION_TYPE_INSTALL_CONTRACT_CODE,
            install_contract_code_args=install_contract_code_args,
        )

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == HostFunctionType.HOST_FUNCTION_TYPE_INVOKE_CONTRACT:
            if self.invoke_args is None:
                raise ValueError("invoke_args should not be None.")
            self.invoke_args.pack(packer)
            return
        if self.type == HostFunctionType.HOST_FUNCTION_TYPE_CREATE_CONTRACT:
            if self.create_contract_args is None:
                raise ValueError("create_contract_args should not be None.")
            self.create_contract_args.pack(packer)
            return
        if self.type == HostFunctionType.HOST_FUNCTION_TYPE_INSTALL_CONTRACT_CODE:
            if self.install_contract_code_args is None:
                raise ValueError("install_contract_code_args should not be None.")
            self.install_contract_code_args.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "HostFunction":
        type = HostFunctionType.unpack(unpacker)
        if type == HostFunctionType.HOST_FUNCTION_TYPE_INVOKE_CONTRACT:
            invoke_args = SCVec.unpack(unpacker)
            return cls(type=type, invoke_args=invoke_args)
        if type == HostFunctionType.HOST_FUNCTION_TYPE_CREATE_CONTRACT:
            create_contract_args = CreateContractArgs.unpack(unpacker)
            return cls(type=type, create_contract_args=create_contract_args)
        if type == HostFunctionType.HOST_FUNCTION_TYPE_INSTALL_CONTRACT_CODE:
            install_contract_code_args = InstallContractCodeArgs.unpack(unpacker)
            return cls(type=type, install_contract_code_args=install_contract_code_args)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "HostFunction":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "HostFunction":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.invoke_args == other.invoke_args
            and self.create_contract_args == other.create_contract_args
            and self.install_contract_code_args == other.install_contract_code_args
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(
            f"invoke_args={self.invoke_args}"
        ) if self.invoke_args is not None else None
        out.append(
            f"create_contract_args={self.create_contract_args}"
        ) if self.create_contract_args is not None else None
        out.append(
            f"install_contract_code_args={self.install_contract_code_args}"
        ) if self.install_contract_code_args is not None else None
        return f"<HostFunction [{', '.join(out)}]>"
