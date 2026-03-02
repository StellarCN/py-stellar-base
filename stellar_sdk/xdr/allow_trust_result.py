# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .allow_trust_result_code import AllowTrustResultCode
from .base import DEFAULT_XDR_MAX_DEPTH

__all__ = ["AllowTrustResult"]


class AllowTrustResult:
    """
    XDR Source Code::

        union AllowTrustResult switch (AllowTrustResultCode code)
        {
        case ALLOW_TRUST_SUCCESS:
            void;
        case ALLOW_TRUST_MALFORMED:
        case ALLOW_TRUST_NO_TRUST_LINE:
        case ALLOW_TRUST_TRUST_NOT_REQUIRED:
        case ALLOW_TRUST_CANT_REVOKE:
        case ALLOW_TRUST_SELF_NOT_ALLOWED:
        case ALLOW_TRUST_LOW_RESERVE:
            void;
        };
    """

    def __init__(
        self,
        code: AllowTrustResultCode,
    ) -> None:
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == AllowTrustResultCode.ALLOW_TRUST_SUCCESS:
            return
        if self.code == AllowTrustResultCode.ALLOW_TRUST_MALFORMED:
            return
        if self.code == AllowTrustResultCode.ALLOW_TRUST_NO_TRUST_LINE:
            return
        if self.code == AllowTrustResultCode.ALLOW_TRUST_TRUST_NOT_REQUIRED:
            return
        if self.code == AllowTrustResultCode.ALLOW_TRUST_CANT_REVOKE:
            return
        if self.code == AllowTrustResultCode.ALLOW_TRUST_SELF_NOT_ALLOWED:
            return
        if self.code == AllowTrustResultCode.ALLOW_TRUST_LOW_RESERVE:
            return
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> AllowTrustResult:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        code = AllowTrustResultCode.unpack(unpacker)
        if code == AllowTrustResultCode.ALLOW_TRUST_SUCCESS:
            return cls(code=code)
        if code == AllowTrustResultCode.ALLOW_TRUST_MALFORMED:
            return cls(code=code)
        if code == AllowTrustResultCode.ALLOW_TRUST_NO_TRUST_LINE:
            return cls(code=code)
        if code == AllowTrustResultCode.ALLOW_TRUST_TRUST_NOT_REQUIRED:
            return cls(code=code)
        if code == AllowTrustResultCode.ALLOW_TRUST_CANT_REVOKE:
            return cls(code=code)
        if code == AllowTrustResultCode.ALLOW_TRUST_SELF_NOT_ALLOWED:
            return cls(code=code)
        if code == AllowTrustResultCode.ALLOW_TRUST_LOW_RESERVE:
            return cls(code=code)
        raise ValueError("Invalid code.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> AllowTrustResult:
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
    def from_xdr(cls, xdr: str) -> AllowTrustResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> AllowTrustResult:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.code == AllowTrustResultCode.ALLOW_TRUST_SUCCESS:
            return "success"
        if self.code == AllowTrustResultCode.ALLOW_TRUST_MALFORMED:
            return "malformed"
        if self.code == AllowTrustResultCode.ALLOW_TRUST_NO_TRUST_LINE:
            return "no_trust_line"
        if self.code == AllowTrustResultCode.ALLOW_TRUST_TRUST_NOT_REQUIRED:
            return "trust_not_required"
        if self.code == AllowTrustResultCode.ALLOW_TRUST_CANT_REVOKE:
            return "cant_revoke"
        if self.code == AllowTrustResultCode.ALLOW_TRUST_SELF_NOT_ALLOWED:
            return "self_not_allowed"
        if self.code == AllowTrustResultCode.ALLOW_TRUST_LOW_RESERVE:
            return "low_reserve"
        raise ValueError(f"Unknown code in AllowTrustResult: {self.code}")

    @classmethod
    def from_json_dict(cls, json_value: str) -> AllowTrustResult:
        if json_value not in (
            "success",
            "malformed",
            "no_trust_line",
            "trust_not_required",
            "cant_revoke",
            "self_not_allowed",
            "low_reserve",
        ):
            raise ValueError(
                f"Unexpected string '{json_value}' for AllowTrustResult, must be one of: success, malformed, no_trust_line, trust_not_required, cant_revoke, self_not_allowed, low_reserve"
            )
        code = AllowTrustResultCode.from_json_dict(json_value)
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
        return f"<AllowTrustResult [{', '.join(out)}]>"
