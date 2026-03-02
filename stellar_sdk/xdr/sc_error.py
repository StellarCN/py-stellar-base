# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .sc_error_code import SCErrorCode
from .sc_error_type import SCErrorType
from .uint32 import Uint32

__all__ = ["SCError"]


class SCError:
    """
    XDR Source Code::

        union SCError switch (SCErrorType type)
        {
        case SCE_CONTRACT:
            uint32 contractCode;
        case SCE_WASM_VM:
        case SCE_CONTEXT:
        case SCE_STORAGE:
        case SCE_OBJECT:
        case SCE_CRYPTO:
        case SCE_EVENTS:
        case SCE_BUDGET:
        case SCE_VALUE:
        case SCE_AUTH:
            SCErrorCode code;
        };
    """

    def __init__(
        self,
        type: SCErrorType,
        contract_code: Optional[Uint32] = None,
        code: Optional[SCErrorCode] = None,
    ) -> None:
        self.type = type
        self.contract_code = contract_code
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == SCErrorType.SCE_CONTRACT:
            if self.contract_code is None:
                raise ValueError("contract_code should not be None.")
            self.contract_code.pack(packer)
            return
        if self.type == SCErrorType.SCE_WASM_VM:
            if self.code is None:
                raise ValueError("code should not be None.")
            self.code.pack(packer)
            return
        if self.type == SCErrorType.SCE_CONTEXT:
            if self.code is None:
                raise ValueError("code should not be None.")
            self.code.pack(packer)
            return
        if self.type == SCErrorType.SCE_STORAGE:
            if self.code is None:
                raise ValueError("code should not be None.")
            self.code.pack(packer)
            return
        if self.type == SCErrorType.SCE_OBJECT:
            if self.code is None:
                raise ValueError("code should not be None.")
            self.code.pack(packer)
            return
        if self.type == SCErrorType.SCE_CRYPTO:
            if self.code is None:
                raise ValueError("code should not be None.")
            self.code.pack(packer)
            return
        if self.type == SCErrorType.SCE_EVENTS:
            if self.code is None:
                raise ValueError("code should not be None.")
            self.code.pack(packer)
            return
        if self.type == SCErrorType.SCE_BUDGET:
            if self.code is None:
                raise ValueError("code should not be None.")
            self.code.pack(packer)
            return
        if self.type == SCErrorType.SCE_VALUE:
            if self.code is None:
                raise ValueError("code should not be None.")
            self.code.pack(packer)
            return
        if self.type == SCErrorType.SCE_AUTH:
            if self.code is None:
                raise ValueError("code should not be None.")
            self.code.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCError:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = SCErrorType.unpack(unpacker)
        if type == SCErrorType.SCE_CONTRACT:
            contract_code = Uint32.unpack(unpacker, depth_limit - 1)
            return cls(type=type, contract_code=contract_code)
        if type == SCErrorType.SCE_WASM_VM:
            code = SCErrorCode.unpack(unpacker)
            return cls(type=type, code=code)
        if type == SCErrorType.SCE_CONTEXT:
            code = SCErrorCode.unpack(unpacker)
            return cls(type=type, code=code)
        if type == SCErrorType.SCE_STORAGE:
            code = SCErrorCode.unpack(unpacker)
            return cls(type=type, code=code)
        if type == SCErrorType.SCE_OBJECT:
            code = SCErrorCode.unpack(unpacker)
            return cls(type=type, code=code)
        if type == SCErrorType.SCE_CRYPTO:
            code = SCErrorCode.unpack(unpacker)
            return cls(type=type, code=code)
        if type == SCErrorType.SCE_EVENTS:
            code = SCErrorCode.unpack(unpacker)
            return cls(type=type, code=code)
        if type == SCErrorType.SCE_BUDGET:
            code = SCErrorCode.unpack(unpacker)
            return cls(type=type, code=code)
        if type == SCErrorType.SCE_VALUE:
            code = SCErrorCode.unpack(unpacker)
            return cls(type=type, code=code)
        if type == SCErrorType.SCE_AUTH:
            code = SCErrorCode.unpack(unpacker)
            return cls(type=type, code=code)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCError:
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
    def from_xdr(cls, xdr: str) -> SCError:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCError:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.type == SCErrorType.SCE_CONTRACT:
            assert self.contract_code is not None
            return {"contract": self.contract_code.to_json_dict()}
        if self.type == SCErrorType.SCE_WASM_VM:
            assert self.code is not None
            return {"wasm_vm": self.code.to_json_dict()}
        if self.type == SCErrorType.SCE_CONTEXT:
            assert self.code is not None
            return {"context": self.code.to_json_dict()}
        if self.type == SCErrorType.SCE_STORAGE:
            assert self.code is not None
            return {"storage": self.code.to_json_dict()}
        if self.type == SCErrorType.SCE_OBJECT:
            assert self.code is not None
            return {"object": self.code.to_json_dict()}
        if self.type == SCErrorType.SCE_CRYPTO:
            assert self.code is not None
            return {"crypto": self.code.to_json_dict()}
        if self.type == SCErrorType.SCE_EVENTS:
            assert self.code is not None
            return {"events": self.code.to_json_dict()}
        if self.type == SCErrorType.SCE_BUDGET:
            assert self.code is not None
            return {"budget": self.code.to_json_dict()}
        if self.type == SCErrorType.SCE_VALUE:
            assert self.code is not None
            return {"value": self.code.to_json_dict()}
        if self.type == SCErrorType.SCE_AUTH:
            assert self.code is not None
            return {"auth": self.code.to_json_dict()}
        raise ValueError(f"Unknown type in SCError: {self.type}")

    @classmethod
    def from_json_dict(cls, json_value: dict) -> SCError:
        if len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for SCError, got: {json_value}"
            )
        key = next(iter(json_value))
        type = SCErrorType.from_json_dict(key)
        if key == "contract":
            contract_code = Uint32.from_json_dict(json_value["contract"])
            return cls(type=type, contract_code=contract_code)
        if key == "wasm_vm":
            code = SCErrorCode.from_json_dict(json_value["wasm_vm"])
            return cls(type=type, code=code)
        if key == "context":
            code = SCErrorCode.from_json_dict(json_value["context"])
            return cls(type=type, code=code)
        if key == "storage":
            code = SCErrorCode.from_json_dict(json_value["storage"])
            return cls(type=type, code=code)
        if key == "object":
            code = SCErrorCode.from_json_dict(json_value["object"])
            return cls(type=type, code=code)
        if key == "crypto":
            code = SCErrorCode.from_json_dict(json_value["crypto"])
            return cls(type=type, code=code)
        if key == "events":
            code = SCErrorCode.from_json_dict(json_value["events"])
            return cls(type=type, code=code)
        if key == "budget":
            code = SCErrorCode.from_json_dict(json_value["budget"])
            return cls(type=type, code=code)
        if key == "value":
            code = SCErrorCode.from_json_dict(json_value["value"])
            return cls(type=type, code=code)
        if key == "auth":
            code = SCErrorCode.from_json_dict(json_value["auth"])
            return cls(type=type, code=code)
        raise ValueError(f"Unknown key '{key}' for SCError")

    def __hash__(self):
        return hash(
            (
                self.type,
                self.contract_code,
                self.code,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.contract_code == other.contract_code
            and self.code == other.code
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        if self.contract_code is not None:
            out.append(f"contract_code={self.contract_code}")
        if self.code is not None:
            out.append(f"code={self.code}")
        return f"<SCError [{', '.join(out)}]>"
