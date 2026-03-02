# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .end_sponsoring_future_reserves_result_code import (
    EndSponsoringFutureReservesResultCode,
)

__all__ = ["EndSponsoringFutureReservesResult"]


class EndSponsoringFutureReservesResult:
    """
    XDR Source Code::

        union EndSponsoringFutureReservesResult switch (
            EndSponsoringFutureReservesResultCode code)
        {
        case END_SPONSORING_FUTURE_RESERVES_SUCCESS:
            void;
        case END_SPONSORING_FUTURE_RESERVES_NOT_SPONSORED:
            void;
        };
    """

    def __init__(
        self,
        code: EndSponsoringFutureReservesResultCode,
    ) -> None:
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if (
            self.code
            == EndSponsoringFutureReservesResultCode.END_SPONSORING_FUTURE_RESERVES_SUCCESS
        ):
            return
        if (
            self.code
            == EndSponsoringFutureReservesResultCode.END_SPONSORING_FUTURE_RESERVES_NOT_SPONSORED
        ):
            return
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> EndSponsoringFutureReservesResult:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        code = EndSponsoringFutureReservesResultCode.unpack(unpacker)
        if (
            code
            == EndSponsoringFutureReservesResultCode.END_SPONSORING_FUTURE_RESERVES_SUCCESS
        ):
            return cls(code=code)
        if (
            code
            == EndSponsoringFutureReservesResultCode.END_SPONSORING_FUTURE_RESERVES_NOT_SPONSORED
        ):
            return cls(code=code)
        raise ValueError("Invalid code.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> EndSponsoringFutureReservesResult:
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
    def from_xdr(cls, xdr: str) -> EndSponsoringFutureReservesResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> EndSponsoringFutureReservesResult:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if (
            self.code
            == EndSponsoringFutureReservesResultCode.END_SPONSORING_FUTURE_RESERVES_SUCCESS
        ):
            return "success"
        if (
            self.code
            == EndSponsoringFutureReservesResultCode.END_SPONSORING_FUTURE_RESERVES_NOT_SPONSORED
        ):
            return "not_sponsored"
        raise ValueError(
            f"Unknown code in EndSponsoringFutureReservesResult: {self.code}"
        )

    @classmethod
    def from_json_dict(cls, json_value: str) -> EndSponsoringFutureReservesResult:
        if json_value not in (
            "success",
            "not_sponsored",
        ):
            raise ValueError(
                f"Unexpected string '{json_value}' for EndSponsoringFutureReservesResult, must be one of: success, not_sponsored"
            )
        code = EndSponsoringFutureReservesResultCode.from_json_dict(json_value)
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
        return f"<EndSponsoringFutureReservesResult [{', '.join(out)}]>"
