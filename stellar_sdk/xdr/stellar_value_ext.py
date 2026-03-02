# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .ledger_close_value_signature import LedgerCloseValueSignature
from .stellar_value_type import StellarValueType

__all__ = ["StellarValueExt"]


class StellarValueExt:
    """
    XDR Source Code::

        union switch (StellarValueType v)
            {
            case STELLAR_VALUE_BASIC:
                void;
            case STELLAR_VALUE_SIGNED:
                LedgerCloseValueSignature lcValueSignature;
            }
    """

    def __init__(
        self,
        v: StellarValueType,
        lc_value_signature: Optional[LedgerCloseValueSignature] = None,
    ) -> None:
        self.v = v
        self.lc_value_signature = lc_value_signature

    def pack(self, packer: Packer) -> None:
        self.v.pack(packer)
        if self.v == StellarValueType.STELLAR_VALUE_BASIC:
            return
        if self.v == StellarValueType.STELLAR_VALUE_SIGNED:
            if self.lc_value_signature is None:
                raise ValueError("lc_value_signature should not be None.")
            self.lc_value_signature.pack(packer)
            return
        raise ValueError("Invalid v.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> StellarValueExt:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        v = StellarValueType.unpack(unpacker)
        if v == StellarValueType.STELLAR_VALUE_BASIC:
            return cls(v=v)
        if v == StellarValueType.STELLAR_VALUE_SIGNED:
            lc_value_signature = LedgerCloseValueSignature.unpack(
                unpacker, depth_limit - 1
            )
            return cls(v=v, lc_value_signature=lc_value_signature)
        raise ValueError("Invalid v.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> StellarValueExt:
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
    def from_xdr(cls, xdr: str) -> StellarValueExt:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> StellarValueExt:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.v == StellarValueType.STELLAR_VALUE_BASIC:
            return "basic"
        if self.v == StellarValueType.STELLAR_VALUE_SIGNED:
            assert self.lc_value_signature is not None
            return {"signed": self.lc_value_signature.to_json_dict()}
        raise ValueError(f"Unknown v in StellarValueExt: {self.v}")

    @classmethod
    def from_json_dict(cls, json_value: str | dict) -> StellarValueExt:
        if isinstance(json_value, str):
            if json_value not in ("basic",):
                raise ValueError(
                    f"Unexpected string '{json_value}' for StellarValueExt, must be one of: basic"
                )
            v = StellarValueType.from_json_dict(json_value)
            return cls(v=v)
        if not isinstance(json_value, dict) or len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for StellarValueExt, got: {json_value}"
            )
        key = next(iter(json_value))
        v = StellarValueType.from_json_dict(key)
        if key == "signed":
            lc_value_signature = LedgerCloseValueSignature.from_json_dict(
                json_value["signed"]
            )
            return cls(v=v, lc_value_signature=lc_value_signature)
        raise ValueError(f"Unknown key '{key}' for StellarValueExt")

    def __hash__(self):
        return hash(
            (
                self.v,
                self.lc_value_signature,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v and self.lc_value_signature == other.lc_value_signature

    def __repr__(self):
        out = []
        out.append(f"v={self.v}")
        if self.lc_value_signature is not None:
            out.append(f"lc_value_signature={self.lc_value_signature}")
        return f"<StellarValueExt [{', '.join(out)}]>"
