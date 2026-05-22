# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .manage_data_result_code import ManageDataResultCode

__all__ = ["ManageDataResult"]


class ManageDataResult:
    """
    XDR Source Code::

        union ManageDataResult switch (ManageDataResultCode code)
        {
        case MANAGE_DATA_SUCCESS:
            void;
        case MANAGE_DATA_NOT_SUPPORTED_YET:
        case MANAGE_DATA_NAME_NOT_FOUND:
        case MANAGE_DATA_LOW_RESERVE:
        case MANAGE_DATA_INVALID_NAME:
            void;
        };
    """

    def __init__(
        self,
        code: ManageDataResultCode,
    ) -> None:
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == ManageDataResultCode.MANAGE_DATA_SUCCESS:
            return
        if self.code == ManageDataResultCode.MANAGE_DATA_NOT_SUPPORTED_YET:
            return
        if self.code == ManageDataResultCode.MANAGE_DATA_NAME_NOT_FOUND:
            return
        if self.code == ManageDataResultCode.MANAGE_DATA_LOW_RESERVE:
            return
        if self.code == ManageDataResultCode.MANAGE_DATA_INVALID_NAME:
            return
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ManageDataResult:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        code = ManageDataResultCode.unpack(unpacker)
        if code == ManageDataResultCode.MANAGE_DATA_SUCCESS:
            return cls(code=code)
        if code == ManageDataResultCode.MANAGE_DATA_NOT_SUPPORTED_YET:
            return cls(code=code)
        if code == ManageDataResultCode.MANAGE_DATA_NAME_NOT_FOUND:
            return cls(code=code)
        if code == ManageDataResultCode.MANAGE_DATA_LOW_RESERVE:
            return cls(code=code)
        if code == ManageDataResultCode.MANAGE_DATA_INVALID_NAME:
            return cls(code=code)
        raise ValueError("Invalid code.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ManageDataResult:
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
    def from_xdr(cls, xdr: str) -> ManageDataResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ManageDataResult:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.code == ManageDataResultCode.MANAGE_DATA_SUCCESS:
            return "success"
        if self.code == ManageDataResultCode.MANAGE_DATA_NOT_SUPPORTED_YET:
            return "not_supported_yet"
        if self.code == ManageDataResultCode.MANAGE_DATA_NAME_NOT_FOUND:
            return "name_not_found"
        if self.code == ManageDataResultCode.MANAGE_DATA_LOW_RESERVE:
            return "low_reserve"
        if self.code == ManageDataResultCode.MANAGE_DATA_INVALID_NAME:
            return "invalid_name"
        raise ValueError(f"Unknown code in ManageDataResult: {self.code}")

    @classmethod
    def from_json_dict(cls, json_value: str) -> ManageDataResult:
        if json_value not in (
            "success",
            "not_supported_yet",
            "name_not_found",
            "low_reserve",
            "invalid_name",
        ):
            raise ValueError(
                f"Unexpected string '{json_value}' for ManageDataResult, must be one of: success, not_supported_yet, name_not_found, low_reserve, invalid_name"
            )
        code = ManageDataResultCode.from_json_dict(json_value)
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
        return f"<ManageDataResult [{', '.join(out)}]>"
