# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .clawback_claimable_balance_result_code import ClawbackClaimableBalanceResultCode

__all__ = ["ClawbackClaimableBalanceResult"]


class ClawbackClaimableBalanceResult:
    """
    XDR Source Code::

        union ClawbackClaimableBalanceResult switch (
            ClawbackClaimableBalanceResultCode code)
        {
        case CLAWBACK_CLAIMABLE_BALANCE_SUCCESS:
            void;
        case CLAWBACK_CLAIMABLE_BALANCE_DOES_NOT_EXIST:
        case CLAWBACK_CLAIMABLE_BALANCE_NOT_ISSUER:
        case CLAWBACK_CLAIMABLE_BALANCE_NOT_CLAWBACK_ENABLED:
            void;
        };
    """

    def __init__(
        self,
        code: ClawbackClaimableBalanceResultCode,
    ) -> None:
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if (
            self.code
            == ClawbackClaimableBalanceResultCode.CLAWBACK_CLAIMABLE_BALANCE_SUCCESS
        ):
            return
        if (
            self.code
            == ClawbackClaimableBalanceResultCode.CLAWBACK_CLAIMABLE_BALANCE_DOES_NOT_EXIST
        ):
            return
        if (
            self.code
            == ClawbackClaimableBalanceResultCode.CLAWBACK_CLAIMABLE_BALANCE_NOT_ISSUER
        ):
            return
        if (
            self.code
            == ClawbackClaimableBalanceResultCode.CLAWBACK_CLAIMABLE_BALANCE_NOT_CLAWBACK_ENABLED
        ):
            return
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ClawbackClaimableBalanceResult:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        code = ClawbackClaimableBalanceResultCode.unpack(unpacker)
        if (
            code
            == ClawbackClaimableBalanceResultCode.CLAWBACK_CLAIMABLE_BALANCE_SUCCESS
        ):
            return cls(code=code)
        if (
            code
            == ClawbackClaimableBalanceResultCode.CLAWBACK_CLAIMABLE_BALANCE_DOES_NOT_EXIST
        ):
            return cls(code=code)
        if (
            code
            == ClawbackClaimableBalanceResultCode.CLAWBACK_CLAIMABLE_BALANCE_NOT_ISSUER
        ):
            return cls(code=code)
        if (
            code
            == ClawbackClaimableBalanceResultCode.CLAWBACK_CLAIMABLE_BALANCE_NOT_CLAWBACK_ENABLED
        ):
            return cls(code=code)
        raise ValueError("Invalid code.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ClawbackClaimableBalanceResult:
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
    def from_xdr(cls, xdr: str) -> ClawbackClaimableBalanceResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ClawbackClaimableBalanceResult:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if (
            self.code
            == ClawbackClaimableBalanceResultCode.CLAWBACK_CLAIMABLE_BALANCE_SUCCESS
        ):
            return "success"
        if (
            self.code
            == ClawbackClaimableBalanceResultCode.CLAWBACK_CLAIMABLE_BALANCE_DOES_NOT_EXIST
        ):
            return "does_not_exist"
        if (
            self.code
            == ClawbackClaimableBalanceResultCode.CLAWBACK_CLAIMABLE_BALANCE_NOT_ISSUER
        ):
            return "not_issuer"
        if (
            self.code
            == ClawbackClaimableBalanceResultCode.CLAWBACK_CLAIMABLE_BALANCE_NOT_CLAWBACK_ENABLED
        ):
            return "not_clawback_enabled"
        raise ValueError(f"Unknown code in ClawbackClaimableBalanceResult: {self.code}")

    @classmethod
    def from_json_dict(cls, json_value: str) -> ClawbackClaimableBalanceResult:
        if json_value not in (
            "success",
            "does_not_exist",
            "not_issuer",
            "not_clawback_enabled",
        ):
            raise ValueError(
                f"Unexpected string '{json_value}' for ClawbackClaimableBalanceResult, must be one of: success, does_not_exist, not_issuer, not_clawback_enabled"
            )
        code = ClawbackClaimableBalanceResultCode.from_json_dict(json_value)
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
        return f"<ClawbackClaimableBalanceResult [{', '.join(out)}]>"
