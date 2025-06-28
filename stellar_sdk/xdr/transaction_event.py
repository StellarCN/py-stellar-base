# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .contract_event import ContractEvent
from .transaction_event_stage import TransactionEventStage

__all__ = ["TransactionEvent"]


class TransactionEvent:
    """
    XDR Source Code::

        struct TransactionEvent {
            TransactionEventStage stage;  // Stage at which an event has occurred.
            ContractEvent event;  // The contract event that has occurred.
        };
    """

    def __init__(
        self,
        stage: TransactionEventStage,
        event: ContractEvent,
    ) -> None:
        self.stage = stage
        self.event = event

    def pack(self, packer: Packer) -> None:
        self.stage.pack(packer)
        self.event.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> TransactionEvent:
        stage = TransactionEventStage.unpack(unpacker)
        event = ContractEvent.unpack(unpacker)
        return cls(
            stage=stage,
            event=event,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TransactionEvent:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> TransactionEvent:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.stage,
                self.event,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.stage == other.stage and self.event == other.event

    def __repr__(self):
        out = [
            f"stage={self.stage}",
            f"event={self.event}",
        ]
        return f"<TransactionEvent [{', '.join(out)}]>"
