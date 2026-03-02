# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .set_trust_line_flags_result_code import SetTrustLineFlagsResultCode

__all__ = ["SetTrustLineFlagsResult"]


class SetTrustLineFlagsResult:
    """
    XDR Source Code::

        union SetTrustLineFlagsResult switch (SetTrustLineFlagsResultCode code)
        {
        case SET_TRUST_LINE_FLAGS_SUCCESS:
            void;
        case SET_TRUST_LINE_FLAGS_MALFORMED:
        case SET_TRUST_LINE_FLAGS_NO_TRUST_LINE:
        case SET_TRUST_LINE_FLAGS_CANT_REVOKE:
        case SET_TRUST_LINE_FLAGS_INVALID_STATE:
        case SET_TRUST_LINE_FLAGS_LOW_RESERVE:
            void;
        };
    """

    def __init__(
        self,
        code: SetTrustLineFlagsResultCode,
    ) -> None:
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_SUCCESS:
            return
        if self.code == SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_MALFORMED:
            return
        if self.code == SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_NO_TRUST_LINE:
            return
        if self.code == SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_CANT_REVOKE:
            return
        if self.code == SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_INVALID_STATE:
            return
        if self.code == SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_LOW_RESERVE:
            return
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SetTrustLineFlagsResult:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        code = SetTrustLineFlagsResultCode.unpack(unpacker)
        if code == SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_SUCCESS:
            return cls(code=code)
        if code == SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_MALFORMED:
            return cls(code=code)
        if code == SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_NO_TRUST_LINE:
            return cls(code=code)
        if code == SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_CANT_REVOKE:
            return cls(code=code)
        if code == SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_INVALID_STATE:
            return cls(code=code)
        if code == SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_LOW_RESERVE:
            return cls(code=code)
        raise ValueError("Invalid code.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SetTrustLineFlagsResult:
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
    def from_xdr(cls, xdr: str) -> SetTrustLineFlagsResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SetTrustLineFlagsResult:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.code == SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_SUCCESS:
            return "success"
        if self.code == SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_MALFORMED:
            return "malformed"
        if self.code == SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_NO_TRUST_LINE:
            return "no_trust_line"
        if self.code == SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_CANT_REVOKE:
            return "cant_revoke"
        if self.code == SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_INVALID_STATE:
            return "invalid_state"
        if self.code == SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_LOW_RESERVE:
            return "low_reserve"
        raise ValueError(f"Unknown code in SetTrustLineFlagsResult: {self.code}")

    @classmethod
    def from_json_dict(cls, json_value: str) -> SetTrustLineFlagsResult:
        if json_value not in (
            "success",
            "malformed",
            "no_trust_line",
            "cant_revoke",
            "invalid_state",
            "low_reserve",
        ):
            raise ValueError(
                f"Unexpected string '{json_value}' for SetTrustLineFlagsResult, must be one of: success, malformed, no_trust_line, cant_revoke, invalid_state, low_reserve"
            )
        code = SetTrustLineFlagsResultCode.from_json_dict(json_value)
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
        return f"<SetTrustLineFlagsResult [{', '.join(out)}]>"
