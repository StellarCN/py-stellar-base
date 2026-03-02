# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List, Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .inflation_payout import InflationPayout
from .inflation_result_code import InflationResultCode

__all__ = ["InflationResult"]


class InflationResult:
    """
    XDR Source Code::

        union InflationResult switch (InflationResultCode code)
        {
        case INFLATION_SUCCESS:
            InflationPayout payouts<>;
        case INFLATION_NOT_TIME:
            void;
        };
    """

    def __init__(
        self,
        code: InflationResultCode,
        payouts: Optional[List[InflationPayout]] = None,
    ) -> None:
        _expect_max_length = 4294967295
        if payouts and len(payouts) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `payouts` should be {_expect_max_length}, but got {len(payouts)}."
            )
        self.code = code
        self.payouts = payouts

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == InflationResultCode.INFLATION_SUCCESS:
            if self.payouts is None:
                raise ValueError("payouts should not be None.")
            packer.pack_uint(len(self.payouts))
            for payouts_item in self.payouts:
                payouts_item.pack(packer)
            return
        if self.code == InflationResultCode.INFLATION_NOT_TIME:
            return
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> InflationResult:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        code = InflationResultCode.unpack(unpacker)
        if code == InflationResultCode.INFLATION_SUCCESS:
            length = unpacker.unpack_uint()
            _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
            if _remaining < length:
                raise ValueError(
                    f"payouts length {length} exceeds remaining input length {_remaining}"
                )
            payouts = []
            for _ in range(length):
                payouts.append(InflationPayout.unpack(unpacker, depth_limit - 1))
            return cls(code=code, payouts=payouts)
        if code == InflationResultCode.INFLATION_NOT_TIME:
            return cls(code=code)
        raise ValueError("Invalid code.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> InflationResult:
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
    def from_xdr(cls, xdr: str) -> InflationResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> InflationResult:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.code == InflationResultCode.INFLATION_SUCCESS:
            assert self.payouts is not None
            return {"success": [item.to_json_dict() for item in self.payouts]}
        if self.code == InflationResultCode.INFLATION_NOT_TIME:
            return "not_time"
        raise ValueError(f"Unknown code in InflationResult: {self.code}")

    @classmethod
    def from_json_dict(cls, json_value: str | dict) -> InflationResult:
        if isinstance(json_value, str):
            if json_value not in ("not_time",):
                raise ValueError(
                    f"Unexpected string '{json_value}' for InflationResult, must be one of: not_time"
                )
            code = InflationResultCode.from_json_dict(json_value)
            return cls(code=code)
        if not isinstance(json_value, dict) or len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for InflationResult, got: {json_value}"
            )
        key = next(iter(json_value))
        code = InflationResultCode.from_json_dict(key)
        if key == "success":
            payouts = [
                InflationPayout.from_json_dict(item) for item in json_value["success"]
            ]
            return cls(code=code, payouts=payouts)
        raise ValueError(f"Unknown key '{key}' for InflationResult")

    def __hash__(self):
        return hash(
            (
                self.code,
                self.payouts,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code and self.payouts == other.payouts

    def __repr__(self):
        out = []
        out.append(f"code={self.code}")
        if self.payouts is not None:
            out.append(f"payouts={self.payouts}")
        return f"<InflationResult [{', '.join(out)}]>"
