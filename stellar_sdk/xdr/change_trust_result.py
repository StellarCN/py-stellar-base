# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .change_trust_result_code import ChangeTrustResultCode

__all__ = ["ChangeTrustResult"]


class ChangeTrustResult:
    """
    XDR Source Code::

        union ChangeTrustResult switch (ChangeTrustResultCode code)
        {
        case CHANGE_TRUST_SUCCESS:
            void;
        case CHANGE_TRUST_MALFORMED:
        case CHANGE_TRUST_NO_ISSUER:
        case CHANGE_TRUST_INVALID_LIMIT:
        case CHANGE_TRUST_LOW_RESERVE:
        case CHANGE_TRUST_SELF_NOT_ALLOWED:
        case CHANGE_TRUST_TRUST_LINE_MISSING:
        case CHANGE_TRUST_CANNOT_DELETE:
        case CHANGE_TRUST_NOT_AUTH_MAINTAIN_LIABILITIES:
            void;
        };
    """

    def __init__(
        self,
        code: ChangeTrustResultCode,
    ) -> None:
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == ChangeTrustResultCode.CHANGE_TRUST_SUCCESS:
            return
        if self.code == ChangeTrustResultCode.CHANGE_TRUST_MALFORMED:
            return
        if self.code == ChangeTrustResultCode.CHANGE_TRUST_NO_ISSUER:
            return
        if self.code == ChangeTrustResultCode.CHANGE_TRUST_INVALID_LIMIT:
            return
        if self.code == ChangeTrustResultCode.CHANGE_TRUST_LOW_RESERVE:
            return
        if self.code == ChangeTrustResultCode.CHANGE_TRUST_SELF_NOT_ALLOWED:
            return
        if self.code == ChangeTrustResultCode.CHANGE_TRUST_TRUST_LINE_MISSING:
            return
        if self.code == ChangeTrustResultCode.CHANGE_TRUST_CANNOT_DELETE:
            return
        if (
            self.code
            == ChangeTrustResultCode.CHANGE_TRUST_NOT_AUTH_MAINTAIN_LIABILITIES
        ):
            return
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ChangeTrustResult:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        code = ChangeTrustResultCode.unpack(unpacker)
        if code == ChangeTrustResultCode.CHANGE_TRUST_SUCCESS:
            return cls(code=code)
        if code == ChangeTrustResultCode.CHANGE_TRUST_MALFORMED:
            return cls(code=code)
        if code == ChangeTrustResultCode.CHANGE_TRUST_NO_ISSUER:
            return cls(code=code)
        if code == ChangeTrustResultCode.CHANGE_TRUST_INVALID_LIMIT:
            return cls(code=code)
        if code == ChangeTrustResultCode.CHANGE_TRUST_LOW_RESERVE:
            return cls(code=code)
        if code == ChangeTrustResultCode.CHANGE_TRUST_SELF_NOT_ALLOWED:
            return cls(code=code)
        if code == ChangeTrustResultCode.CHANGE_TRUST_TRUST_LINE_MISSING:
            return cls(code=code)
        if code == ChangeTrustResultCode.CHANGE_TRUST_CANNOT_DELETE:
            return cls(code=code)
        if code == ChangeTrustResultCode.CHANGE_TRUST_NOT_AUTH_MAINTAIN_LIABILITIES:
            return cls(code=code)
        raise ValueError("Invalid code.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ChangeTrustResult:
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
    def from_xdr(cls, xdr: str) -> ChangeTrustResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ChangeTrustResult:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.code == ChangeTrustResultCode.CHANGE_TRUST_SUCCESS:
            return "success"
        if self.code == ChangeTrustResultCode.CHANGE_TRUST_MALFORMED:
            return "malformed"
        if self.code == ChangeTrustResultCode.CHANGE_TRUST_NO_ISSUER:
            return "no_issuer"
        if self.code == ChangeTrustResultCode.CHANGE_TRUST_INVALID_LIMIT:
            return "invalid_limit"
        if self.code == ChangeTrustResultCode.CHANGE_TRUST_LOW_RESERVE:
            return "low_reserve"
        if self.code == ChangeTrustResultCode.CHANGE_TRUST_SELF_NOT_ALLOWED:
            return "self_not_allowed"
        if self.code == ChangeTrustResultCode.CHANGE_TRUST_TRUST_LINE_MISSING:
            return "trust_line_missing"
        if self.code == ChangeTrustResultCode.CHANGE_TRUST_CANNOT_DELETE:
            return "cannot_delete"
        if (
            self.code
            == ChangeTrustResultCode.CHANGE_TRUST_NOT_AUTH_MAINTAIN_LIABILITIES
        ):
            return "not_auth_maintain_liabilities"
        raise ValueError(f"Unknown code in ChangeTrustResult: {self.code}")

    @classmethod
    def from_json_dict(cls, json_value: str) -> ChangeTrustResult:
        if json_value not in (
            "success",
            "malformed",
            "no_issuer",
            "invalid_limit",
            "low_reserve",
            "self_not_allowed",
            "trust_line_missing",
            "cannot_delete",
            "not_auth_maintain_liabilities",
        ):
            raise ValueError(
                f"Unexpected string '{json_value}' for ChangeTrustResult, must be one of: success, malformed, no_issuer, invalid_limit, low_reserve, self_not_allowed, trust_line_missing, cannot_delete, not_auth_maintain_liabilities"
            )
        code = ChangeTrustResultCode.from_json_dict(json_value)
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
        return f"<ChangeTrustResult [{', '.join(out)}]>"
