# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .begin_sponsoring_future_reserves_result_code import (
    BeginSponsoringFutureReservesResultCode,
)

__all__ = ["BeginSponsoringFutureReservesResult"]


class BeginSponsoringFutureReservesResult:
    """
    XDR Source Code::

        union BeginSponsoringFutureReservesResult switch (
            BeginSponsoringFutureReservesResultCode code)
        {
        case BEGIN_SPONSORING_FUTURE_RESERVES_SUCCESS:
            void;
        case BEGIN_SPONSORING_FUTURE_RESERVES_MALFORMED:
        case BEGIN_SPONSORING_FUTURE_RESERVES_ALREADY_SPONSORED:
        case BEGIN_SPONSORING_FUTURE_RESERVES_RECURSIVE:
            void;
        };
    """

    def __init__(
        self,
        code: BeginSponsoringFutureReservesResultCode,
    ) -> None:
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if (
            self.code
            == BeginSponsoringFutureReservesResultCode.BEGIN_SPONSORING_FUTURE_RESERVES_SUCCESS
        ):
            return
        if (
            self.code
            == BeginSponsoringFutureReservesResultCode.BEGIN_SPONSORING_FUTURE_RESERVES_MALFORMED
        ):
            return
        if (
            self.code
            == BeginSponsoringFutureReservesResultCode.BEGIN_SPONSORING_FUTURE_RESERVES_ALREADY_SPONSORED
        ):
            return
        if (
            self.code
            == BeginSponsoringFutureReservesResultCode.BEGIN_SPONSORING_FUTURE_RESERVES_RECURSIVE
        ):
            return
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> BeginSponsoringFutureReservesResult:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        code = BeginSponsoringFutureReservesResultCode.unpack(unpacker)
        if (
            code
            == BeginSponsoringFutureReservesResultCode.BEGIN_SPONSORING_FUTURE_RESERVES_SUCCESS
        ):
            return cls(code=code)
        if (
            code
            == BeginSponsoringFutureReservesResultCode.BEGIN_SPONSORING_FUTURE_RESERVES_MALFORMED
        ):
            return cls(code=code)
        if (
            code
            == BeginSponsoringFutureReservesResultCode.BEGIN_SPONSORING_FUTURE_RESERVES_ALREADY_SPONSORED
        ):
            return cls(code=code)
        if (
            code
            == BeginSponsoringFutureReservesResultCode.BEGIN_SPONSORING_FUTURE_RESERVES_RECURSIVE
        ):
            return cls(code=code)
        raise ValueError("Invalid code.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> BeginSponsoringFutureReservesResult:
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
    def from_xdr(cls, xdr: str) -> BeginSponsoringFutureReservesResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> BeginSponsoringFutureReservesResult:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if (
            self.code
            == BeginSponsoringFutureReservesResultCode.BEGIN_SPONSORING_FUTURE_RESERVES_SUCCESS
        ):
            return "success"
        if (
            self.code
            == BeginSponsoringFutureReservesResultCode.BEGIN_SPONSORING_FUTURE_RESERVES_MALFORMED
        ):
            return "malformed"
        if (
            self.code
            == BeginSponsoringFutureReservesResultCode.BEGIN_SPONSORING_FUTURE_RESERVES_ALREADY_SPONSORED
        ):
            return "already_sponsored"
        if (
            self.code
            == BeginSponsoringFutureReservesResultCode.BEGIN_SPONSORING_FUTURE_RESERVES_RECURSIVE
        ):
            return "recursive"
        raise ValueError(
            f"Unknown code in BeginSponsoringFutureReservesResult: {self.code}"
        )

    @classmethod
    def from_json_dict(cls, json_value: str) -> BeginSponsoringFutureReservesResult:
        if json_value not in (
            "success",
            "malformed",
            "already_sponsored",
            "recursive",
        ):
            raise ValueError(
                f"Unexpected string '{json_value}' for BeginSponsoringFutureReservesResult, must be one of: success, malformed, already_sponsored, recursive"
            )
        code = BeginSponsoringFutureReservesResultCode.from_json_dict(json_value)
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
        return f"<BeginSponsoringFutureReservesResult [{', '.join(out)}]>"
