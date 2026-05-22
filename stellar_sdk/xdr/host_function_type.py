# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_HOST_FUNCTION_TYPE_MAP = {
    0: "invoke_contract",
    1: "create_contract",
    2: "upload_contract_wasm",
    3: "create_contract_v2",
}
_HOST_FUNCTION_TYPE_REVERSE_MAP = {
    "invoke_contract": 0,
    "create_contract": 1,
    "upload_contract_wasm": 2,
    "create_contract_v2": 3,
}
__all__ = ["HostFunctionType"]


class HostFunctionType(IntEnum):
    """
    XDR Source Code::

        enum HostFunctionType
        {
            HOST_FUNCTION_TYPE_INVOKE_CONTRACT = 0,
            HOST_FUNCTION_TYPE_CREATE_CONTRACT = 1,
            HOST_FUNCTION_TYPE_UPLOAD_CONTRACT_WASM = 2,
            HOST_FUNCTION_TYPE_CREATE_CONTRACT_V2 = 3
        };
    """

    HOST_FUNCTION_TYPE_INVOKE_CONTRACT = 0
    HOST_FUNCTION_TYPE_CREATE_CONTRACT = 1
    HOST_FUNCTION_TYPE_UPLOAD_CONTRACT_WASM = 2
    HOST_FUNCTION_TYPE_CREATE_CONTRACT_V2 = 3

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> HostFunctionType:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> HostFunctionType:
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
    def from_xdr(cls, xdr: str) -> HostFunctionType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> HostFunctionType:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _HOST_FUNCTION_TYPE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> HostFunctionType:
        return cls(_HOST_FUNCTION_TYPE_REVERSE_MAP[json_value])
