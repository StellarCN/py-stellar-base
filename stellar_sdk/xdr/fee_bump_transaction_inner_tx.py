# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

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
        v1: TransactionV1Envelope = None,
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

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> FeeBumpTransactionInnerTx:
        type = EnvelopeType.unpack(unpacker)
        if type == EnvelopeType.ENVELOPE_TYPE_TX:
            v1 = TransactionV1Envelope.unpack(unpacker)
            return cls(type=type, v1=v1)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> FeeBumpTransactionInnerTx:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> FeeBumpTransactionInnerTx:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
        out.append(f"v1={self.v1}") if self.v1 is not None else None
        return f"<FeeBumpTransactionInnerTx [{', '.join(out)}]>"
