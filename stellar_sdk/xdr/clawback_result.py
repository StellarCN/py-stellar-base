# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .clawback_result_code import ClawbackResultCode

__all__ = ["ClawbackResult"]


class ClawbackResult:
    """
    XDR Source Code::

        union ClawbackResult switch (ClawbackResultCode code)
        {
        case CLAWBACK_SUCCESS:
            void;
        case CLAWBACK_MALFORMED:
        case CLAWBACK_NOT_CLAWBACK_ENABLED:
        case CLAWBACK_NO_TRUST:
        case CLAWBACK_UNDERFUNDED:
            void;
        };
    """

    def __init__(
        self,
        code: ClawbackResultCode,
    ) -> None:
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == ClawbackResultCode.CLAWBACK_SUCCESS:
            return
        if self.code == ClawbackResultCode.CLAWBACK_MALFORMED:
            return
        if self.code == ClawbackResultCode.CLAWBACK_NOT_CLAWBACK_ENABLED:
            return
        if self.code == ClawbackResultCode.CLAWBACK_NO_TRUST:
            return
        if self.code == ClawbackResultCode.CLAWBACK_UNDERFUNDED:
            return
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ClawbackResult:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        code = ClawbackResultCode.unpack(unpacker)
        if code == ClawbackResultCode.CLAWBACK_SUCCESS:
            return cls(code=code)
        if code == ClawbackResultCode.CLAWBACK_MALFORMED:
            return cls(code=code)
        if code == ClawbackResultCode.CLAWBACK_NOT_CLAWBACK_ENABLED:
            return cls(code=code)
        if code == ClawbackResultCode.CLAWBACK_NO_TRUST:
            return cls(code=code)
        if code == ClawbackResultCode.CLAWBACK_UNDERFUNDED:
            return cls(code=code)
        raise ValueError("Invalid code.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ClawbackResult:
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
    def from_xdr(cls, xdr: str) -> ClawbackResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ClawbackResult:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.code == ClawbackResultCode.CLAWBACK_SUCCESS:
            return "success"
        if self.code == ClawbackResultCode.CLAWBACK_MALFORMED:
            return "malformed"
        if self.code == ClawbackResultCode.CLAWBACK_NOT_CLAWBACK_ENABLED:
            return "not_clawback_enabled"
        if self.code == ClawbackResultCode.CLAWBACK_NO_TRUST:
            return "no_trust"
        if self.code == ClawbackResultCode.CLAWBACK_UNDERFUNDED:
            return "underfunded"
        raise ValueError(f"Unknown code in ClawbackResult: {self.code}")

    @classmethod
    def from_json_dict(cls, json_value: str) -> ClawbackResult:
        if json_value not in (
            "success",
            "malformed",
            "not_clawback_enabled",
            "no_trust",
            "underfunded",
        ):
            raise ValueError(
                f"Unexpected string '{json_value}' for ClawbackResult, must be one of: success, malformed, not_clawback_enabled, no_trust, underfunded"
            )
        code = ClawbackResultCode.from_json_dict(json_value)
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
        return f"<ClawbackResult [{', '.join(out)}]>"
