# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .claim_claimable_balance_result_code import ClaimClaimableBalanceResultCode

__all__ = ["ClaimClaimableBalanceResult"]


class ClaimClaimableBalanceResult:
    """
    XDR Source Code::

        union ClaimClaimableBalanceResult switch (ClaimClaimableBalanceResultCode code)
        {
        case CLAIM_CLAIMABLE_BALANCE_SUCCESS:
            void;
        case CLAIM_CLAIMABLE_BALANCE_DOES_NOT_EXIST:
        case CLAIM_CLAIMABLE_BALANCE_CANNOT_CLAIM:
        case CLAIM_CLAIMABLE_BALANCE_LINE_FULL:
        case CLAIM_CLAIMABLE_BALANCE_NO_TRUST:
        case CLAIM_CLAIMABLE_BALANCE_NOT_AUTHORIZED:
        case CLAIM_CLAIMABLE_BALANCE_TRUSTLINE_FROZEN:
            void;
        };
    """

    def __init__(
        self,
        code: ClaimClaimableBalanceResultCode,
    ) -> None:
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_SUCCESS:
            return
        if (
            self.code
            == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_DOES_NOT_EXIST
        ):
            return
        if (
            self.code
            == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_CANNOT_CLAIM
        ):
            return
        if (
            self.code
            == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_LINE_FULL
        ):
            return
        if (
            self.code
            == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_NO_TRUST
        ):
            return
        if (
            self.code
            == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_NOT_AUTHORIZED
        ):
            return
        if (
            self.code
            == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_TRUSTLINE_FROZEN
        ):
            return
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ClaimClaimableBalanceResult:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        code = ClaimClaimableBalanceResultCode.unpack(unpacker)
        if code == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_SUCCESS:
            return cls(code=code)
        if (
            code
            == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_DOES_NOT_EXIST
        ):
            return cls(code=code)
        if code == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_CANNOT_CLAIM:
            return cls(code=code)
        if code == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_LINE_FULL:
            return cls(code=code)
        if code == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_NO_TRUST:
            return cls(code=code)
        if (
            code
            == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_NOT_AUTHORIZED
        ):
            return cls(code=code)
        if (
            code
            == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_TRUSTLINE_FROZEN
        ):
            return cls(code=code)
        raise ValueError("Invalid code.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ClaimClaimableBalanceResult:
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
    def from_xdr(cls, xdr: str) -> ClaimClaimableBalanceResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ClaimClaimableBalanceResult:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.code == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_SUCCESS:
            return "success"
        if (
            self.code
            == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_DOES_NOT_EXIST
        ):
            return "does_not_exist"
        if (
            self.code
            == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_CANNOT_CLAIM
        ):
            return "cannot_claim"
        if (
            self.code
            == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_LINE_FULL
        ):
            return "line_full"
        if (
            self.code
            == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_NO_TRUST
        ):
            return "no_trust"
        if (
            self.code
            == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_NOT_AUTHORIZED
        ):
            return "not_authorized"
        if (
            self.code
            == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_TRUSTLINE_FROZEN
        ):
            return "trustline_frozen"
        raise ValueError(f"Unknown code in ClaimClaimableBalanceResult: {self.code}")

    @classmethod
    def from_json_dict(cls, json_value: str) -> ClaimClaimableBalanceResult:
        if json_value not in (
            "success",
            "does_not_exist",
            "cannot_claim",
            "line_full",
            "no_trust",
            "not_authorized",
            "trustline_frozen",
        ):
            raise ValueError(
                f"Unexpected string '{json_value}' for ClaimClaimableBalanceResult, must be one of: success, does_not_exist, cannot_claim, line_full, no_trust, not_authorized, trustline_frozen"
            )
        code = ClaimClaimableBalanceResultCode.from_json_dict(json_value)
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
        return f"<ClaimClaimableBalanceResult [{', '.join(out)}]>"
