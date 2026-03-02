# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .envelope_type import EnvelopeType
from .transaction_v1_envelope import TransactionV1Envelope

__all__ = ["FeeBumpTransactionInnerTx"]


class FeeBumpTransactionInnerTx:
    """
    XDR Source Code::

        union switch (EnvelopeType type)
            {
            case ENVELOPE_TYPE_TX:
                TransactionV1Envelope v1;
            }
    """

    def __init__(
        self,
        type: EnvelopeType,
        v1: Optional[TransactionV1Envelope] = None,
    ) -> None:
        self.type = type
        self.v1 = v1

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == EnvelopeType.ENVELOPE_TYPE_TX:
            if self.v1 is None:
                raise ValueError("v1 should not be None.")
            self.v1.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> FeeBumpTransactionInnerTx:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = EnvelopeType.unpack(unpacker)
        if type == EnvelopeType.ENVELOPE_TYPE_TX:
            v1 = TransactionV1Envelope.unpack(unpacker, depth_limit - 1)
            return cls(type=type, v1=v1)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> FeeBumpTransactionInnerTx:
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
    def from_xdr(cls, xdr: str) -> FeeBumpTransactionInnerTx:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> FeeBumpTransactionInnerTx:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.type == EnvelopeType.ENVELOPE_TYPE_TX:
            assert self.v1 is not None
            return {"tx": self.v1.to_json_dict()}
        raise ValueError(f"Unknown type in FeeBumpTransactionInnerTx: {self.type}")

    @classmethod
    def from_json_dict(cls, json_value: dict) -> FeeBumpTransactionInnerTx:
        if len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for FeeBumpTransactionInnerTx, got: {json_value}"
            )
        key = next(iter(json_value))
        type = EnvelopeType.from_json_dict(key)
        if key == "tx":
            v1 = TransactionV1Envelope.from_json_dict(json_value["tx"])
            return cls(type=type, v1=v1)
        raise ValueError(f"Unknown key '{key}' for FeeBumpTransactionInnerTx")

    def __hash__(self):
        return hash(
            (
                self.type,
                self.v1,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.type == other.type and self.v1 == other.v1

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        if self.v1 is not None:
            out.append(f"v1={self.v1}")
        return f"<FeeBumpTransactionInnerTx [{', '.join(out)}]>"
