# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .begin_sponsoring_future_reserves_result_code import (
    BeginSponsoringFutureReservesResultCode,
)
from ..exceptions import ValueError

__all__ = ["BeginSponsoringFutureReservesResult"]


class BeginSponsoringFutureReservesResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union BeginSponsoringFutureReservesResult switch (BeginSponsoringFutureReservesResultCode code)
    {
    case BEGIN_SPONSORING_FUTURE_RESERVES_SUCCESS:
        void;
    default:
        void;
    };
    ----------------------------------------------------------------
    """

    def __init__(self, code: BeginSponsoringFutureReservesResultCode,) -> None:
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if (
            self.code
            == BeginSponsoringFutureReservesResultCode.BEGIN_SPONSORING_FUTURE_RESERVES_SUCCESS
        ):
            return
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "BeginSponsoringFutureReservesResult":
        code = BeginSponsoringFutureReservesResultCode.unpack(unpacker)
        if (
            code
            == BeginSponsoringFutureReservesResultCode.BEGIN_SPONSORING_FUTURE_RESERVES_SUCCESS
        ):
            return cls(code)
        raise ValueError("Invalid code.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "BeginSponsoringFutureReservesResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "BeginSponsoringFutureReservesResult":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code

    def __str__(self):
        out = []
        out.append(f"code={self.code}")
        return f"<BeginSponsoringFutureReservesResult {[', '.join(out)]}>"
