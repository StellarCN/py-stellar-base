# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .restore_footprint_result_code import RestoreFootprintResultCode

__all__ = ["RestoreFootprintResult"]


class RestoreFootprintResult:
    """
    XDR Source Code::

        union RestoreFootprintResult switch (RestoreFootprintResultCode code)
        {
        case RESTORE_FOOTPRINT_SUCCESS:
            void;
        case RESTORE_FOOTPRINT_MALFORMED:
        case RESTORE_FOOTPRINT_RESOURCE_LIMIT_EXCEEDED:
        case RESTORE_FOOTPRINT_INSUFFICIENT_REFUNDABLE_FEE:
            void;
        };
    """

    def __init__(
        self,
        code: RestoreFootprintResultCode,
    ) -> None:
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == RestoreFootprintResultCode.RESTORE_FOOTPRINT_SUCCESS:
            return
        if self.code == RestoreFootprintResultCode.RESTORE_FOOTPRINT_MALFORMED:
            return
        if (
            self.code
            == RestoreFootprintResultCode.RESTORE_FOOTPRINT_RESOURCE_LIMIT_EXCEEDED
        ):
            return
        if (
            self.code
            == RestoreFootprintResultCode.RESTORE_FOOTPRINT_INSUFFICIENT_REFUNDABLE_FEE
        ):
            return
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> RestoreFootprintResult:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        code = RestoreFootprintResultCode.unpack(unpacker)
        if code == RestoreFootprintResultCode.RESTORE_FOOTPRINT_SUCCESS:
            return cls(code=code)
        if code == RestoreFootprintResultCode.RESTORE_FOOTPRINT_MALFORMED:
            return cls(code=code)
        if code == RestoreFootprintResultCode.RESTORE_FOOTPRINT_RESOURCE_LIMIT_EXCEEDED:
            return cls(code=code)
        if (
            code
            == RestoreFootprintResultCode.RESTORE_FOOTPRINT_INSUFFICIENT_REFUNDABLE_FEE
        ):
            return cls(code=code)
        raise ValueError("Invalid code.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> RestoreFootprintResult:
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
    def from_xdr(cls, xdr: str) -> RestoreFootprintResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> RestoreFootprintResult:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.code == RestoreFootprintResultCode.RESTORE_FOOTPRINT_SUCCESS:
            return "success"
        if self.code == RestoreFootprintResultCode.RESTORE_FOOTPRINT_MALFORMED:
            return "malformed"
        if (
            self.code
            == RestoreFootprintResultCode.RESTORE_FOOTPRINT_RESOURCE_LIMIT_EXCEEDED
        ):
            return "resource_limit_exceeded"
        if (
            self.code
            == RestoreFootprintResultCode.RESTORE_FOOTPRINT_INSUFFICIENT_REFUNDABLE_FEE
        ):
            return "insufficient_refundable_fee"
        raise ValueError(f"Unknown code in RestoreFootprintResult: {self.code}")

    @classmethod
    def from_json_dict(cls, json_value: str) -> RestoreFootprintResult:
        if json_value not in (
            "success",
            "malformed",
            "resource_limit_exceeded",
            "insufficient_refundable_fee",
        ):
            raise ValueError(
                f"Unexpected string '{json_value}' for RestoreFootprintResult, must be one of: success, malformed, resource_limit_exceeded, insufficient_refundable_fee"
            )
        code = RestoreFootprintResultCode.from_json_dict(json_value)
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
        return f"<RestoreFootprintResult [{', '.join(out)}]>"
