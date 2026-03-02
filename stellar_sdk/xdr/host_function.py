# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, Opaque
from .create_contract_args import CreateContractArgs
from .create_contract_args_v2 import CreateContractArgsV2
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
        case HOST_FUNCTION_TYPE_CREATE_CONTRACT_V2:
            CreateContractArgsV2 createContractV2;
        };
    """

    def __init__(
        self,
        type: HostFunctionType,
        invoke_contract: Optional[InvokeContractArgs] = None,
        create_contract: Optional[CreateContractArgs] = None,
        wasm: Optional[bytes] = None,
        create_contract_v2: Optional[CreateContractArgsV2] = None,
    ) -> None:
        _expect_max_length = 4294967295
        if wasm and len(wasm) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `wasm` should be {_expect_max_length}, but got {len(wasm)}."
            )
        self.type = type
        self.invoke_contract = invoke_contract
        self.create_contract = create_contract
        self.wasm = wasm
        self.create_contract_v2 = create_contract_v2

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
        if self.type == HostFunctionType.HOST_FUNCTION_TYPE_CREATE_CONTRACT_V2:
            if self.create_contract_v2 is None:
                raise ValueError("create_contract_v2 should not be None.")
            self.create_contract_v2.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> HostFunction:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = HostFunctionType.unpack(unpacker)
        if type == HostFunctionType.HOST_FUNCTION_TYPE_INVOKE_CONTRACT:
            invoke_contract = InvokeContractArgs.unpack(unpacker, depth_limit - 1)
            return cls(type=type, invoke_contract=invoke_contract)
        if type == HostFunctionType.HOST_FUNCTION_TYPE_CREATE_CONTRACT:
            create_contract = CreateContractArgs.unpack(unpacker, depth_limit - 1)
            return cls(type=type, create_contract=create_contract)
        if type == HostFunctionType.HOST_FUNCTION_TYPE_UPLOAD_CONTRACT_WASM:
            wasm = Opaque.unpack(unpacker, 4294967295, False)
            return cls(type=type, wasm=wasm)
        if type == HostFunctionType.HOST_FUNCTION_TYPE_CREATE_CONTRACT_V2:
            create_contract_v2 = CreateContractArgsV2.unpack(unpacker, depth_limit - 1)
            return cls(type=type, create_contract_v2=create_contract_v2)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> HostFunction:
        unpacker = Unpacker(xdr)
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> HostFunction:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> HostFunction:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.type == HostFunctionType.HOST_FUNCTION_TYPE_INVOKE_CONTRACT:
            assert self.invoke_contract is not None
            return {"invoke_contract": self.invoke_contract.to_json_dict()}
        if self.type == HostFunctionType.HOST_FUNCTION_TYPE_CREATE_CONTRACT:
            assert self.create_contract is not None
            return {"create_contract": self.create_contract.to_json_dict()}
        if self.type == HostFunctionType.HOST_FUNCTION_TYPE_UPLOAD_CONTRACT_WASM:
            assert self.wasm is not None
            return {"upload_contract_wasm": Opaque.to_json_dict(self.wasm)}
        if self.type == HostFunctionType.HOST_FUNCTION_TYPE_CREATE_CONTRACT_V2:
            assert self.create_contract_v2 is not None
            return {"create_contract_v2": self.create_contract_v2.to_json_dict()}
        raise ValueError(f"Unknown type in HostFunction: {self.type}")

    @classmethod
    def from_json_dict(cls, json_value: dict) -> HostFunction:
        if len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for HostFunction, got: {json_value}"
            )
        key = next(iter(json_value))
        type = HostFunctionType.from_json_dict(key)
        if key == "invoke_contract":
            invoke_contract = InvokeContractArgs.from_json_dict(
                json_value["invoke_contract"]
            )
            return cls(type=type, invoke_contract=invoke_contract)
        if key == "create_contract":
            create_contract = CreateContractArgs.from_json_dict(
                json_value["create_contract"]
            )
            return cls(type=type, create_contract=create_contract)
        if key == "upload_contract_wasm":
            wasm = Opaque.from_json_dict(json_value["upload_contract_wasm"])
            return cls(type=type, wasm=wasm)
        if key == "create_contract_v2":
            create_contract_v2 = CreateContractArgsV2.from_json_dict(
                json_value["create_contract_v2"]
            )
            return cls(type=type, create_contract_v2=create_contract_v2)
        raise ValueError(f"Unknown key '{key}' for HostFunction")

    def __hash__(self):
        return hash(
            (
                self.type,
                self.invoke_contract,
                self.create_contract,
                self.wasm,
                self.create_contract_v2,
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
            and self.create_contract_v2 == other.create_contract_v2
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        if self.invoke_contract is not None:
            out.append(f"invoke_contract={self.invoke_contract}")
        if self.create_contract is not None:
            out.append(f"create_contract={self.create_contract}")
        if self.wasm is not None:
            out.append(f"wasm={self.wasm}")
        if self.create_contract_v2 is not None:
            out.append(f"create_contract_v2={self.create_contract_v2}")
        return f"<HostFunction [{', '.join(out)}]>"
