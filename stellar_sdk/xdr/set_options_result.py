# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .set_options_result_code import SetOptionsResultCode

__all__ = ["SetOptionsResult"]


class SetOptionsResult:
    """
    XDR Source Code::

        union SetOptionsResult switch (SetOptionsResultCode code)
        {
        case SET_OPTIONS_SUCCESS:
            void;
        case SET_OPTIONS_LOW_RESERVE:
        case SET_OPTIONS_TOO_MANY_SIGNERS:
        case SET_OPTIONS_BAD_FLAGS:
        case SET_OPTIONS_INVALID_INFLATION:
        case SET_OPTIONS_CANT_CHANGE:
        case SET_OPTIONS_UNKNOWN_FLAG:
        case SET_OPTIONS_THRESHOLD_OUT_OF_RANGE:
        case SET_OPTIONS_BAD_SIGNER:
        case SET_OPTIONS_INVALID_HOME_DOMAIN:
        case SET_OPTIONS_AUTH_REVOCABLE_REQUIRED:
            void;
        };
    """

    def __init__(
        self,
        code: SetOptionsResultCode,
    ) -> None:
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == SetOptionsResultCode.SET_OPTIONS_SUCCESS:
            return
        if self.code == SetOptionsResultCode.SET_OPTIONS_LOW_RESERVE:
            return
        if self.code == SetOptionsResultCode.SET_OPTIONS_TOO_MANY_SIGNERS:
            return
        if self.code == SetOptionsResultCode.SET_OPTIONS_BAD_FLAGS:
            return
        if self.code == SetOptionsResultCode.SET_OPTIONS_INVALID_INFLATION:
            return
        if self.code == SetOptionsResultCode.SET_OPTIONS_CANT_CHANGE:
            return
        if self.code == SetOptionsResultCode.SET_OPTIONS_UNKNOWN_FLAG:
            return
        if self.code == SetOptionsResultCode.SET_OPTIONS_THRESHOLD_OUT_OF_RANGE:
            return
        if self.code == SetOptionsResultCode.SET_OPTIONS_BAD_SIGNER:
            return
        if self.code == SetOptionsResultCode.SET_OPTIONS_INVALID_HOME_DOMAIN:
            return
        if self.code == SetOptionsResultCode.SET_OPTIONS_AUTH_REVOCABLE_REQUIRED:
            return
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SetOptionsResult:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        code = SetOptionsResultCode.unpack(unpacker)
        if code == SetOptionsResultCode.SET_OPTIONS_SUCCESS:
            return cls(code=code)
        if code == SetOptionsResultCode.SET_OPTIONS_LOW_RESERVE:
            return cls(code=code)
        if code == SetOptionsResultCode.SET_OPTIONS_TOO_MANY_SIGNERS:
            return cls(code=code)
        if code == SetOptionsResultCode.SET_OPTIONS_BAD_FLAGS:
            return cls(code=code)
        if code == SetOptionsResultCode.SET_OPTIONS_INVALID_INFLATION:
            return cls(code=code)
        if code == SetOptionsResultCode.SET_OPTIONS_CANT_CHANGE:
            return cls(code=code)
        if code == SetOptionsResultCode.SET_OPTIONS_UNKNOWN_FLAG:
            return cls(code=code)
        if code == SetOptionsResultCode.SET_OPTIONS_THRESHOLD_OUT_OF_RANGE:
            return cls(code=code)
        if code == SetOptionsResultCode.SET_OPTIONS_BAD_SIGNER:
            return cls(code=code)
        if code == SetOptionsResultCode.SET_OPTIONS_INVALID_HOME_DOMAIN:
            return cls(code=code)
        if code == SetOptionsResultCode.SET_OPTIONS_AUTH_REVOCABLE_REQUIRED:
            return cls(code=code)
        raise ValueError("Invalid code.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SetOptionsResult:
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
    def from_xdr(cls, xdr: str) -> SetOptionsResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SetOptionsResult:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.code == SetOptionsResultCode.SET_OPTIONS_SUCCESS:
            return "success"
        if self.code == SetOptionsResultCode.SET_OPTIONS_LOW_RESERVE:
            return "low_reserve"
        if self.code == SetOptionsResultCode.SET_OPTIONS_TOO_MANY_SIGNERS:
            return "too_many_signers"
        if self.code == SetOptionsResultCode.SET_OPTIONS_BAD_FLAGS:
            return "bad_flags"
        if self.code == SetOptionsResultCode.SET_OPTIONS_INVALID_INFLATION:
            return "invalid_inflation"
        if self.code == SetOptionsResultCode.SET_OPTIONS_CANT_CHANGE:
            return "cant_change"
        if self.code == SetOptionsResultCode.SET_OPTIONS_UNKNOWN_FLAG:
            return "unknown_flag"
        if self.code == SetOptionsResultCode.SET_OPTIONS_THRESHOLD_OUT_OF_RANGE:
            return "threshold_out_of_range"
        if self.code == SetOptionsResultCode.SET_OPTIONS_BAD_SIGNER:
            return "bad_signer"
        if self.code == SetOptionsResultCode.SET_OPTIONS_INVALID_HOME_DOMAIN:
            return "invalid_home_domain"
        if self.code == SetOptionsResultCode.SET_OPTIONS_AUTH_REVOCABLE_REQUIRED:
            return "auth_revocable_required"
        raise ValueError(f"Unknown code in SetOptionsResult: {self.code}")

    @classmethod
    def from_json_dict(cls, json_value: str) -> SetOptionsResult:
        if json_value not in (
            "success",
            "low_reserve",
            "too_many_signers",
            "bad_flags",
            "invalid_inflation",
            "cant_change",
            "unknown_flag",
            "threshold_out_of_range",
            "bad_signer",
            "invalid_home_domain",
            "auth_revocable_required",
        ):
            raise ValueError(
                f"Unexpected string '{json_value}' for SetOptionsResult, must be one of: success, low_reserve, too_many_signers, bad_flags, invalid_inflation, cant_change, unknown_flag, threshold_out_of_range, bad_signer, invalid_home_domain, auth_revocable_required"
            )
        code = SetOptionsResultCode.from_json_dict(json_value)
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
        return f"<SetOptionsResult [{', '.join(out)}]>"
