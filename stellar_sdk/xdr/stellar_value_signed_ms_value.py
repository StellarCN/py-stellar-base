# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .ledger_close_value_signature import LedgerCloseValueSignature
from .time_point_ms import TimePointMs

__all__ = ["StellarValueSignedMsValue"]


class StellarValueSignedMsValue:
    """
    XDR Source Code::

        struct
                {
                    TimePointMs closeTimeMs; // closeTime == closeTimeMs / 1000
                    LedgerCloseValueSignature lcValueSignature;
                }
    """

    def __init__(
        self,
        close_time_ms: TimePointMs,
        lc_value_signature: LedgerCloseValueSignature,
    ) -> None:
        self.close_time_ms = close_time_ms
        self.lc_value_signature = lc_value_signature

    def pack(self, packer: Packer) -> None:
        self.close_time_ms.pack(packer)
        self.lc_value_signature.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> StellarValueSignedMsValue:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        close_time_ms = TimePointMs.unpack(unpacker, depth_limit - 1)
        lc_value_signature = LedgerCloseValueSignature.unpack(unpacker, depth_limit - 1)
        return cls(
            close_time_ms=close_time_ms,
            lc_value_signature=lc_value_signature,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> StellarValueSignedMsValue:
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
    def from_xdr(cls, xdr: str) -> StellarValueSignedMsValue:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> StellarValueSignedMsValue:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "close_time_ms": self.close_time_ms.to_json_dict(),
            "lc_value_signature": self.lc_value_signature.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> StellarValueSignedMsValue:
        close_time_ms = TimePointMs.from_json_dict(json_dict["close_time_ms"])
        lc_value_signature = LedgerCloseValueSignature.from_json_dict(
            json_dict["lc_value_signature"]
        )
        return cls(
            close_time_ms=close_time_ms,
            lc_value_signature=lc_value_signature,
        )

    def __hash__(self):
        return hash(
            (
                self.close_time_ms,
                self.lc_value_signature,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.close_time_ms == other.close_time_ms
            and self.lc_value_signature == other.lc_value_signature
        )

    def __repr__(self):
        out = [
            f"close_time_ms={self.close_time_ms}",
            f"lc_value_signature={self.lc_value_signature}",
        ]
        return f"<StellarValueSignedMsValue [{', '.join(out)}]>"
