# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .contract_executable_external_ref import ContractExecutableExternalRef
from .contract_executable_type import ContractExecutableType
from .hash import Hash

__all__ = ["ContractExecutable"]


class ContractExecutable:
    """
    XDR Source Code::

        union ContractExecutable switch (ContractExecutableType type)
        {
        case CONTRACT_EXECUTABLE_WASM:
            Hash wasm_hash;
        case CONTRACT_EXECUTABLE_STELLAR_ASSET:
            void;
        case CONTRACT_EXECUTABLE_EXTERNAL_REF:
            ContractExecutableExternalRef external_ref;
        };
    """

    def __init__(
        self,
        type: ContractExecutableType,
        wasm_hash: Hash | None = None,
        external_ref: ContractExecutableExternalRef | None = None,
    ) -> None:
        self.type = type
        self.wasm_hash = wasm_hash
        self.external_ref = external_ref

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == ContractExecutableType.CONTRACT_EXECUTABLE_WASM:
            if self.wasm_hash is None:
                raise ValueError("wasm_hash should not be None.")
            self.wasm_hash.pack(packer)
            return
        if self.type == ContractExecutableType.CONTRACT_EXECUTABLE_STELLAR_ASSET:
            return
        if self.type == ContractExecutableType.CONTRACT_EXECUTABLE_EXTERNAL_REF:
            if self.external_ref is None:
                raise ValueError("external_ref should not be None.")
            self.external_ref.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ContractExecutable:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = ContractExecutableType.unpack(unpacker)
        if type == ContractExecutableType.CONTRACT_EXECUTABLE_WASM:
            wasm_hash = Hash.unpack(unpacker, depth_limit - 1)
            return cls(type=type, wasm_hash=wasm_hash)
        if type == ContractExecutableType.CONTRACT_EXECUTABLE_STELLAR_ASSET:
            return cls(type=type)
        if type == ContractExecutableType.CONTRACT_EXECUTABLE_EXTERNAL_REF:
            external_ref = ContractExecutableExternalRef.unpack(
                unpacker, depth_limit - 1
            )
            return cls(type=type, external_ref=external_ref)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ContractExecutable:
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
    def from_xdr(cls, xdr: str) -> ContractExecutable:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ContractExecutable:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.type == ContractExecutableType.CONTRACT_EXECUTABLE_WASM:
            assert self.wasm_hash is not None
            return {"wasm": self.wasm_hash.to_json_dict()}
        if self.type == ContractExecutableType.CONTRACT_EXECUTABLE_STELLAR_ASSET:
            return "stellar_asset"
        if self.type == ContractExecutableType.CONTRACT_EXECUTABLE_EXTERNAL_REF:
            assert self.external_ref is not None
            return {"external_ref": self.external_ref.to_json_dict()}
        raise ValueError(f"Unknown type in ContractExecutable: {self.type}")

    @classmethod
    def from_json_dict(cls, json_value: str | dict) -> ContractExecutable:
        if isinstance(json_value, str):
            if json_value not in ("stellar_asset",):
                raise ValueError(
                    f"Unexpected string '{json_value}' for ContractExecutable, must be one of: stellar_asset"
                )
            type = ContractExecutableType.from_json_dict(json_value)
            return cls(type=type)
        if not isinstance(json_value, dict) or len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for ContractExecutable, got: {json_value}"
            )
        key = next(iter(json_value))
        type = ContractExecutableType.from_json_dict(key)
        if key == "wasm":
            wasm_hash = Hash.from_json_dict(json_value["wasm"])
            return cls(type=type, wasm_hash=wasm_hash)
        if key == "external_ref":
            external_ref = ContractExecutableExternalRef.from_json_dict(
                json_value["external_ref"]
            )
            return cls(type=type, external_ref=external_ref)
        raise ValueError(f"Unknown key '{key}' for ContractExecutable")

    def __hash__(self):
        return hash(
            (
                self.type,
                self.wasm_hash,
                self.external_ref,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.wasm_hash == other.wasm_hash
            and self.external_ref == other.external_ref
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        if self.wasm_hash is not None:
            out.append(f"wasm_hash={self.wasm_hash}")
        if self.external_ref is not None:
            out.append(f"external_ref={self.external_ref}")
        return f"<ContractExecutable [{', '.join(out)}]>"
