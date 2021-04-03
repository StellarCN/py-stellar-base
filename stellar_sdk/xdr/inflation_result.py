# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib import Packer, Unpacker

from .inflation_payout import InflationPayout
from .inflation_result_code import InflationResultCode
from ..exceptions import ValueError

__all__ = ["InflationResult"]


class InflationResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union InflationResult switch (InflationResultCode code)
    {
    case INFLATION_SUCCESS:
        InflationPayout payouts<>;
    default:
        void;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        code: InflationResultCode,
        payouts: List[InflationPayout] = None,
    ) -> None:
        if payouts and len(payouts) > 4294967295:
            raise ValueError(
                f"The maximum length of `payouts` should be 4294967295, but got {len(payouts)}."
            )
        self.code = code
        self.payouts = payouts

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == InflationResultCode.INFLATION_SUCCESS:
            if self.payouts is None:
                raise ValueError("payouts should not be None.")
            packer.pack_uint(len(self.payouts))
            for payout in self.payouts:
                payout.pack(packer)
            return
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "InflationResult":
        code = InflationResultCode.unpack(unpacker)
        if code == InflationResultCode.INFLATION_SUCCESS:
            length = unpacker.unpack_uint()
            payouts = []
            for _ in range(length):
                payouts.append(InflationPayout.unpack(unpacker))
            return cls(code, payouts=payouts)
        raise ValueError("Invalid code.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "InflationResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "InflationResult":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code and self.payouts == other.payouts

    def __str__(self):
        out = []
        out.append(f"code={self.code}")
        out.append(f"payouts={self.payouts}") if self.payouts is not None else None
        return f"<InflationResult {[', '.join(out)]}>"
