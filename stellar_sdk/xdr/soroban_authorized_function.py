# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .create_contract_args import CreateContractArgs
from .create_contract_args_v2 import CreateContractArgsV2
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
        // This variant of auth payload for creating new contract instances
        // doesn't allow specifying the constructor arguments, creating contracts
        // with constructors that take arguments is only possible by authorizing
        // `SOROBAN_AUTHORIZED_FUNCTION_TYPE_CREATE_CONTRACT_V2_HOST_FN`
        // (protocol 22+).
        case SOROBAN_AUTHORIZED_FUNCTION_TYPE_CREATE_CONTRACT_HOST_FN:
            CreateContractArgs createContractHostFn;
        // This variant of auth payload for creating new contract instances
        // is only accepted in and after protocol 22. It allows authorizing the
        // contract constructor arguments.
        case SOROBAN_AUTHORIZED_FUNCTION_TYPE_CREATE_CONTRACT_V2_HOST_FN:
            CreateContractArgsV2 createContractV2HostFn;
        };
    """

    def __init__(
        self,
        type: SorobanAuthorizedFunctionType,
        contract_fn: Optional[InvokeContractArgs] = None,
        create_contract_host_fn: Optional[CreateContractArgs] = None,
        create_contract_v2_host_fn: Optional[CreateContractArgsV2] = None,
    ) -> None:
        self.type = type
        self.contract_fn = contract_fn
        self.create_contract_host_fn = create_contract_host_fn
        self.create_contract_v2_host_fn = create_contract_v2_host_fn

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
        if (
            self.type
            == SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CREATE_CONTRACT_V2_HOST_FN
        ):
            if self.create_contract_v2_host_fn is None:
                raise ValueError("create_contract_v2_host_fn should not be None.")
            self.create_contract_v2_host_fn.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SorobanAuthorizedFunction:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = SorobanAuthorizedFunctionType.unpack(unpacker)
        if (
            type
            == SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN
        ):
            contract_fn = InvokeContractArgs.unpack(unpacker, depth_limit - 1)
            return cls(type=type, contract_fn=contract_fn)
        if (
            type
            == SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CREATE_CONTRACT_HOST_FN
        ):
            create_contract_host_fn = CreateContractArgs.unpack(
                unpacker, depth_limit - 1
            )
            return cls(type=type, create_contract_host_fn=create_contract_host_fn)
        if (
            type
            == SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CREATE_CONTRACT_V2_HOST_FN
        ):
            create_contract_v2_host_fn = CreateContractArgsV2.unpack(
                unpacker, depth_limit - 1
            )
            return cls(type=type, create_contract_v2_host_fn=create_contract_v2_host_fn)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SorobanAuthorizedFunction:
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
    def from_xdr(cls, xdr: str) -> SorobanAuthorizedFunction:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SorobanAuthorizedFunction:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if (
            self.type
            == SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN
        ):
            assert self.contract_fn is not None
            return {"contract_fn": self.contract_fn.to_json_dict()}
        if (
            self.type
            == SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CREATE_CONTRACT_HOST_FN
        ):
            assert self.create_contract_host_fn is not None
            return {
                "create_contract_host_fn": self.create_contract_host_fn.to_json_dict()
            }
        if (
            self.type
            == SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CREATE_CONTRACT_V2_HOST_FN
        ):
            assert self.create_contract_v2_host_fn is not None
            return {
                "create_contract_v2_host_fn": self.create_contract_v2_host_fn.to_json_dict()
            }
        raise ValueError(f"Unknown type in SorobanAuthorizedFunction: {self.type}")

    @classmethod
    def from_json_dict(cls, json_value: dict) -> SorobanAuthorizedFunction:
        if len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for SorobanAuthorizedFunction, got: {json_value}"
            )
        key = next(iter(json_value))
        type = SorobanAuthorizedFunctionType.from_json_dict(key)
        if key == "contract_fn":
            contract_fn = InvokeContractArgs.from_json_dict(json_value["contract_fn"])
            return cls(type=type, contract_fn=contract_fn)
        if key == "create_contract_host_fn":
            create_contract_host_fn = CreateContractArgs.from_json_dict(
                json_value["create_contract_host_fn"]
            )
            return cls(type=type, create_contract_host_fn=create_contract_host_fn)
        if key == "create_contract_v2_host_fn":
            create_contract_v2_host_fn = CreateContractArgsV2.from_json_dict(
                json_value["create_contract_v2_host_fn"]
            )
            return cls(type=type, create_contract_v2_host_fn=create_contract_v2_host_fn)
        raise ValueError(f"Unknown key '{key}' for SorobanAuthorizedFunction")

    def __hash__(self):
        return hash(
            (
                self.type,
                self.contract_fn,
                self.create_contract_host_fn,
                self.create_contract_v2_host_fn,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.contract_fn == other.contract_fn
            and self.create_contract_host_fn == other.create_contract_host_fn
            and self.create_contract_v2_host_fn == other.create_contract_v2_host_fn
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        if self.contract_fn is not None:
            out.append(f"contract_fn={self.contract_fn}")
        if self.create_contract_host_fn is not None:
            out.append(f"create_contract_host_fn={self.create_contract_host_fn}")
        if self.create_contract_v2_host_fn is not None:
            out.append(f"create_contract_v2_host_fn={self.create_contract_v2_host_fn}")
        return f"<SorobanAuthorizedFunction [{', '.join(out)}]>"
