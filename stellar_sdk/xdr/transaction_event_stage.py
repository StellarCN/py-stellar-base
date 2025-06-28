# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

__all__ = ["TransactionEventStage"]


class TransactionEventStage(IntEnum):
    """
    XDR Source Code::

        enum TransactionEventStage {
            // The event has happened before any one of the transactions has its
            // operations applied.
            TRANSACTION_EVENT_STAGE_BEFORE_ALL_TXS = 0,
            // The event has happened immediately after operations of the transaction
            // have been applied.
            TRANSACTION_EVENT_STAGE_AFTER_TX = 1,
            // The event has happened after every transaction had its operations
            // applied.
            TRANSACTION_EVENT_STAGE_AFTER_ALL_TXS = 2
        };
    """

    TRANSACTION_EVENT_STAGE_BEFORE_ALL_TXS = 0
    TRANSACTION_EVENT_STAGE_AFTER_TX = 1
    TRANSACTION_EVENT_STAGE_AFTER_ALL_TXS = 2

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> TransactionEventStage:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TransactionEventStage:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> TransactionEventStage:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
