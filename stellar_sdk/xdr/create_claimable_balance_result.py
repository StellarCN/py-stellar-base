# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .claimable_balance_id import ClaimableBalanceID
from .create_claimable_balance_result_code import CreateClaimableBalanceResultCode

__all__ = ["CreateClaimableBalanceResult"]


class CreateClaimableBalanceResult:
    """
    XDR Source Code::

        union CreateClaimableBalanceResult switch (
            CreateClaimableBalanceResultCode code)
        {
        case CREATE_CLAIMABLE_BALANCE_SUCCESS:
            ClaimableBalanceID balanceID;
        case CREATE_CLAIMABLE_BALANCE_MALFORMED:
        case CREATE_CLAIMABLE_BALANCE_LOW_RESERVE:
        case CREATE_CLAIMABLE_BALANCE_NO_TRUST:
        case CREATE_CLAIMABLE_BALANCE_NOT_AUTHORIZED:
        case CREATE_CLAIMABLE_BALANCE_UNDERFUNDED:
            void;
        };
    """

    def __init__(
        self,
        code: CreateClaimableBalanceResultCode,
        balance_id: Optional[ClaimableBalanceID] = None,
    ) -> None:
        self.code = code
        self.balance_id = balance_id

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if (
            self.code
            == CreateClaimableBalanceResultCode.CREATE_CLAIMABLE_BALANCE_SUCCESS
        ):
            if self.balance_id is None:
                raise ValueError("balance_id should not be None.")
            self.balance_id.pack(packer)
            return
        if (
            self.code
            == CreateClaimableBalanceResultCode.CREATE_CLAIMABLE_BALANCE_MALFORMED
        ):
            return
        if (
            self.code
            == CreateClaimableBalanceResultCode.CREATE_CLAIMABLE_BALANCE_LOW_RESERVE
        ):
            return
        if (
            self.code
            == CreateClaimableBalanceResultCode.CREATE_CLAIMABLE_BALANCE_NO_TRUST
        ):
            return
        if (
            self.code
            == CreateClaimableBalanceResultCode.CREATE_CLAIMABLE_BALANCE_NOT_AUTHORIZED
        ):
            return
        if (
            self.code
            == CreateClaimableBalanceResultCode.CREATE_CLAIMABLE_BALANCE_UNDERFUNDED
        ):
            return
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> CreateClaimableBalanceResult:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        code = CreateClaimableBalanceResultCode.unpack(unpacker)
        if code == CreateClaimableBalanceResultCode.CREATE_CLAIMABLE_BALANCE_SUCCESS:
            balance_id = ClaimableBalanceID.unpack(unpacker, depth_limit - 1)
            return cls(code=code, balance_id=balance_id)
        if code == CreateClaimableBalanceResultCode.CREATE_CLAIMABLE_BALANCE_MALFORMED:
            return cls(code=code)
        if (
            code
            == CreateClaimableBalanceResultCode.CREATE_CLAIMABLE_BALANCE_LOW_RESERVE
        ):
            return cls(code=code)
        if code == CreateClaimableBalanceResultCode.CREATE_CLAIMABLE_BALANCE_NO_TRUST:
            return cls(code=code)
        if (
            code
            == CreateClaimableBalanceResultCode.CREATE_CLAIMABLE_BALANCE_NOT_AUTHORIZED
        ):
            return cls(code=code)
        if (
            code
            == CreateClaimableBalanceResultCode.CREATE_CLAIMABLE_BALANCE_UNDERFUNDED
        ):
            return cls(code=code)
        raise ValueError("Invalid code.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> CreateClaimableBalanceResult:
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
    def from_xdr(cls, xdr: str) -> CreateClaimableBalanceResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> CreateClaimableBalanceResult:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if (
            self.code
            == CreateClaimableBalanceResultCode.CREATE_CLAIMABLE_BALANCE_SUCCESS
        ):
            assert self.balance_id is not None
            return {"success": self.balance_id.to_json_dict()}
        if (
            self.code
            == CreateClaimableBalanceResultCode.CREATE_CLAIMABLE_BALANCE_MALFORMED
        ):
            return "malformed"
        if (
            self.code
            == CreateClaimableBalanceResultCode.CREATE_CLAIMABLE_BALANCE_LOW_RESERVE
        ):
            return "low_reserve"
        if (
            self.code
            == CreateClaimableBalanceResultCode.CREATE_CLAIMABLE_BALANCE_NO_TRUST
        ):
            return "no_trust"
        if (
            self.code
            == CreateClaimableBalanceResultCode.CREATE_CLAIMABLE_BALANCE_NOT_AUTHORIZED
        ):
            return "not_authorized"
        if (
            self.code
            == CreateClaimableBalanceResultCode.CREATE_CLAIMABLE_BALANCE_UNDERFUNDED
        ):
            return "underfunded"
        raise ValueError(f"Unknown code in CreateClaimableBalanceResult: {self.code}")

    @classmethod
    def from_json_dict(cls, json_value: str | dict) -> CreateClaimableBalanceResult:
        if isinstance(json_value, str):
            if json_value not in (
                "malformed",
                "low_reserve",
                "no_trust",
                "not_authorized",
                "underfunded",
            ):
                raise ValueError(
                    f"Unexpected string '{json_value}' for CreateClaimableBalanceResult, must be one of: malformed, low_reserve, no_trust, not_authorized, underfunded"
                )
            code = CreateClaimableBalanceResultCode.from_json_dict(json_value)
            return cls(code=code)
        if not isinstance(json_value, dict) or len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for CreateClaimableBalanceResult, got: {json_value}"
            )
        key = next(iter(json_value))
        code = CreateClaimableBalanceResultCode.from_json_dict(key)
        if key == "success":
            balance_id = ClaimableBalanceID.from_json_dict(json_value["success"])
            return cls(code=code, balance_id=balance_id)
        raise ValueError(f"Unknown key '{key}' for CreateClaimableBalanceResult")

    def __hash__(self):
        return hash(
            (
                self.code,
                self.balance_id,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code and self.balance_id == other.balance_id

    def __repr__(self):
        out = []
        out.append(f"code={self.code}")
        if self.balance_id is not None:
            out.append(f"balance_id={self.balance_id}")
        return f"<CreateClaimableBalanceResult [{', '.join(out)}]>"
