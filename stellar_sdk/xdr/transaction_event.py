# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> TransactionEvent:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        stage = TransactionEventStage.unpack(unpacker)
        event = ContractEvent.unpack(unpacker, depth_limit - 1)
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> TransactionEvent:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TransactionEvent:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "stage": self.stage.to_json_dict(),
            "event": self.event.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> TransactionEvent:
        stage = TransactionEventStage.from_json_dict(json_dict["stage"])
        event = ContractEvent.from_json_dict(json_dict["event"])
        return cls(
            stage=stage,
            event=event,
        )

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
