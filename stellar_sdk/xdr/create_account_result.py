# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .create_account_result_code import CreateAccountResultCode

__all__ = ["CreateAccountResult"]


class CreateAccountResult:
    """
    XDR Source Code::

        union CreateAccountResult switch (CreateAccountResultCode code)
        {
        case CREATE_ACCOUNT_SUCCESS:
            void;
        case CREATE_ACCOUNT_MALFORMED:
        case CREATE_ACCOUNT_UNDERFUNDED:
        case CREATE_ACCOUNT_LOW_RESERVE:
        case CREATE_ACCOUNT_ALREADY_EXIST:
            void;
        };
    """

    def __init__(
        self,
        code: CreateAccountResultCode,
    ) -> None:
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == CreateAccountResultCode.CREATE_ACCOUNT_SUCCESS:
            return
        if self.code == CreateAccountResultCode.CREATE_ACCOUNT_MALFORMED:
            return
        if self.code == CreateAccountResultCode.CREATE_ACCOUNT_UNDERFUNDED:
            return
        if self.code == CreateAccountResultCode.CREATE_ACCOUNT_LOW_RESERVE:
            return
        if self.code == CreateAccountResultCode.CREATE_ACCOUNT_ALREADY_EXIST:
            return
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> CreateAccountResult:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        code = CreateAccountResultCode.unpack(unpacker)
        if code == CreateAccountResultCode.CREATE_ACCOUNT_SUCCESS:
            return cls(code=code)
        if code == CreateAccountResultCode.CREATE_ACCOUNT_MALFORMED:
            return cls(code=code)
        if code == CreateAccountResultCode.CREATE_ACCOUNT_UNDERFUNDED:
            return cls(code=code)
        if code == CreateAccountResultCode.CREATE_ACCOUNT_LOW_RESERVE:
            return cls(code=code)
        if code == CreateAccountResultCode.CREATE_ACCOUNT_ALREADY_EXIST:
            return cls(code=code)
        raise ValueError("Invalid code.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> CreateAccountResult:
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
    def from_xdr(cls, xdr: str) -> CreateAccountResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> CreateAccountResult:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.code == CreateAccountResultCode.CREATE_ACCOUNT_SUCCESS:
            return "success"
        if self.code == CreateAccountResultCode.CREATE_ACCOUNT_MALFORMED:
            return "malformed"
        if self.code == CreateAccountResultCode.CREATE_ACCOUNT_UNDERFUNDED:
            return "underfunded"
        if self.code == CreateAccountResultCode.CREATE_ACCOUNT_LOW_RESERVE:
            return "low_reserve"
        if self.code == CreateAccountResultCode.CREATE_ACCOUNT_ALREADY_EXIST:
            return "already_exist"
        raise ValueError(f"Unknown code in CreateAccountResult: {self.code}")

    @classmethod
    def from_json_dict(cls, json_value: str) -> CreateAccountResult:
        if json_value not in (
            "success",
            "malformed",
            "underfunded",
            "low_reserve",
            "already_exist",
        ):
            raise ValueError(
                f"Unexpected string '{json_value}' for CreateAccountResult, must be one of: success, malformed, underfunded, low_reserve, already_exist"
            )
        code = CreateAccountResultCode.from_json_dict(json_value)
        return cls(code=code)

    def __hash__(self):
        return hash((self.code,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code

    def __repr__(self):
        out = []
        out.append(f"code={self.code}")
        return f"<CreateAccountResult [{', '.join(out)}]>"
