# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .hash import Hash
from .invoke_host_function_result_code import InvokeHostFunctionResultCode

__all__ = ["InvokeHostFunctionResult"]


class InvokeHostFunctionResult:
    """
    XDR Source Code::

        union InvokeHostFunctionResult switch (InvokeHostFunctionResultCode code)
        {
        case INVOKE_HOST_FUNCTION_SUCCESS:
            Hash success; // sha256(InvokeHostFunctionSuccessPreImage)
        case INVOKE_HOST_FUNCTION_MALFORMED:
        case INVOKE_HOST_FUNCTION_TRAPPED:
        case INVOKE_HOST_FUNCTION_RESOURCE_LIMIT_EXCEEDED:
        case INVOKE_HOST_FUNCTION_ENTRY_ARCHIVED:
        case INVOKE_HOST_FUNCTION_INSUFFICIENT_REFUNDABLE_FEE:
            void;
        };
    """

    def __init__(
        self,
        code: InvokeHostFunctionResultCode,
        success: Optional[Hash] = None,
    ) -> None:
        self.code = code
        self.success = success

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == InvokeHostFunctionResultCode.INVOKE_HOST_FUNCTION_SUCCESS:
            if self.success is None:
                raise ValueError("success should not be None.")
            self.success.pack(packer)
            return
        if self.code == InvokeHostFunctionResultCode.INVOKE_HOST_FUNCTION_MALFORMED:
            return
        if self.code == InvokeHostFunctionResultCode.INVOKE_HOST_FUNCTION_TRAPPED:
            return
        if (
            self.code
            == InvokeHostFunctionResultCode.INVOKE_HOST_FUNCTION_RESOURCE_LIMIT_EXCEEDED
        ):
            return
        if (
            self.code
            == InvokeHostFunctionResultCode.INVOKE_HOST_FUNCTION_ENTRY_ARCHIVED
        ):
            return
        if (
            self.code
            == InvokeHostFunctionResultCode.INVOKE_HOST_FUNCTION_INSUFFICIENT_REFUNDABLE_FEE
        ):
            return
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> InvokeHostFunctionResult:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        code = InvokeHostFunctionResultCode.unpack(unpacker)
        if code == InvokeHostFunctionResultCode.INVOKE_HOST_FUNCTION_SUCCESS:
            success = Hash.unpack(unpacker, depth_limit - 1)
            return cls(code=code, success=success)
        if code == InvokeHostFunctionResultCode.INVOKE_HOST_FUNCTION_MALFORMED:
            return cls(code=code)
        if code == InvokeHostFunctionResultCode.INVOKE_HOST_FUNCTION_TRAPPED:
            return cls(code=code)
        if (
            code
            == InvokeHostFunctionResultCode.INVOKE_HOST_FUNCTION_RESOURCE_LIMIT_EXCEEDED
        ):
            return cls(code=code)
        if code == InvokeHostFunctionResultCode.INVOKE_HOST_FUNCTION_ENTRY_ARCHIVED:
            return cls(code=code)
        if (
            code
            == InvokeHostFunctionResultCode.INVOKE_HOST_FUNCTION_INSUFFICIENT_REFUNDABLE_FEE
        ):
            return cls(code=code)
        raise ValueError("Invalid code.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> InvokeHostFunctionResult:
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
    def from_xdr(cls, xdr: str) -> InvokeHostFunctionResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> InvokeHostFunctionResult:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.code == InvokeHostFunctionResultCode.INVOKE_HOST_FUNCTION_SUCCESS:
            assert self.success is not None
            return {"success": self.success.to_json_dict()}
        if self.code == InvokeHostFunctionResultCode.INVOKE_HOST_FUNCTION_MALFORMED:
            return "malformed"
        if self.code == InvokeHostFunctionResultCode.INVOKE_HOST_FUNCTION_TRAPPED:
            return "trapped"
        if (
            self.code
            == InvokeHostFunctionResultCode.INVOKE_HOST_FUNCTION_RESOURCE_LIMIT_EXCEEDED
        ):
            return "resource_limit_exceeded"
        if (
            self.code
            == InvokeHostFunctionResultCode.INVOKE_HOST_FUNCTION_ENTRY_ARCHIVED
        ):
            return "entry_archived"
        if (
            self.code
            == InvokeHostFunctionResultCode.INVOKE_HOST_FUNCTION_INSUFFICIENT_REFUNDABLE_FEE
        ):
            return "insufficient_refundable_fee"
        raise ValueError(f"Unknown code in InvokeHostFunctionResult: {self.code}")

    @classmethod
    def from_json_dict(cls, json_value: str | dict) -> InvokeHostFunctionResult:
        if isinstance(json_value, str):
            if json_value not in (
                "malformed",
                "trapped",
                "resource_limit_exceeded",
                "entry_archived",
                "insufficient_refundable_fee",
            ):
                raise ValueError(
                    f"Unexpected string '{json_value}' for InvokeHostFunctionResult, must be one of: malformed, trapped, resource_limit_exceeded, entry_archived, insufficient_refundable_fee"
                )
            code = InvokeHostFunctionResultCode.from_json_dict(json_value)
            return cls(code=code)
        if not isinstance(json_value, dict) or len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for InvokeHostFunctionResult, got: {json_value}"
            )
        key = next(iter(json_value))
        code = InvokeHostFunctionResultCode.from_json_dict(key)
        if key == "success":
            success = Hash.from_json_dict(json_value["success"])
            return cls(code=code, success=success)
        raise ValueError(f"Unknown key '{key}' for InvokeHostFunctionResult")

    def __hash__(self):
        return hash(
            (
                self.code,
                self.success,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code and self.success == other.success

    def __repr__(self):
        out = []
        out.append(f"code={self.code}")
        if self.success is not None:
            out.append(f"success={self.success}")
        return f"<InvokeHostFunctionResult [{', '.join(out)}]>"
