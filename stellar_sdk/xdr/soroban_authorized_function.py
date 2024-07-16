# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .create_contract_args import CreateContractArgs
from .invoke_contract_args import InvokeContractArgs
from .soroban_authorized_function_type import SorobanAuthorizedFunctionType

__all__ = ["SorobanAuthorizedFunction"]


class SorobanAuthorizedFunction:
    """
    XDR Source Code::

        union SorobanAuthorizedFunction switch (SorobanAuthorizedFunctionType type)
        {
        case SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN:
            InvokeContractArgs contractFn;
        case SOROBAN_AUTHORIZED_FUNCTION_TYPE_CREATE_CONTRACT_HOST_FN:
            CreateContractArgs createContractHostFn;
        };
    """

    def __init__(
        self,
        type: SorobanAuthorizedFunctionType,
        contract_fn: InvokeContractArgs = None,
        create_contract_host_fn: CreateContractArgs = None,
    ) -> None:
        self.type = type
        self.contract_fn = contract_fn
        self.create_contract_host_fn = create_contract_host_fn

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if (
            self.type
            == SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN
        ):
            if self.contract_fn is None:
                raise ValueError("contract_fn should not be None.")
            self.contract_fn.pack(packer)
            return
        if (
            self.type
            == SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CREATE_CONTRACT_HOST_FN
        ):
            if self.create_contract_host_fn is None:
                raise ValueError("create_contract_host_fn should not be None.")
            self.create_contract_host_fn.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SorobanAuthorizedFunction:
        type = SorobanAuthorizedFunctionType.unpack(unpacker)
        if (
            type
            == SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN
        ):
            contract_fn = InvokeContractArgs.unpack(unpacker)
            return cls(type=type, contract_fn=contract_fn)
        if (
            type
            == SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CREATE_CONTRACT_HOST_FN
        ):
            create_contract_host_fn = CreateContractArgs.unpack(unpacker)
            return cls(type=type, create_contract_host_fn=create_contract_host_fn)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SorobanAuthorizedFunction:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SorobanAuthorizedFunction:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.type,
                self.contract_fn,
                self.create_contract_host_fn,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.contract_fn == other.contract_fn
            and self.create_contract_host_fn == other.create_contract_host_fn
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        (
            out.append(f"contract_fn={self.contract_fn}")
            if self.contract_fn is not None
            else None
        )
        (
            out.append(f"create_contract_host_fn={self.create_contract_host_fn}")
            if self.create_contract_host_fn is not None
            else None
        )
        return f"<SorobanAuthorizedFunction [{', '.join(out)}]>"
