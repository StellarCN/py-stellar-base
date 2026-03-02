# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, Boolean
from .contract_event import ContractEvent

__all__ = ["DiagnosticEvent"]


class DiagnosticEvent:
    """
    XDR Source Code::

        struct DiagnosticEvent
        {
            bool inSuccessfulContractCall;
            ContractEvent event;
        };
    """

    def __init__(
        self,
        in_successful_contract_call: bool,
        event: ContractEvent,
    ) -> None:
        self.in_successful_contract_call = in_successful_contract_call
        self.event = event

    def pack(self, packer: Packer) -> None:
        Boolean(self.in_successful_contract_call).pack(packer)
        self.event.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> DiagnosticEvent:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        in_successful_contract_call = Boolean.unpack(unpacker)
        event = ContractEvent.unpack(unpacker, depth_limit - 1)
        return cls(
            in_successful_contract_call=in_successful_contract_call,
            event=event,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> DiagnosticEvent:
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
    def from_xdr(cls, xdr: str) -> DiagnosticEvent:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> DiagnosticEvent:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "in_successful_contract_call": Boolean.to_json_dict(
                self.in_successful_contract_call
            ),
            "event": self.event.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> DiagnosticEvent:
        in_successful_contract_call = Boolean.from_json_dict(
            json_dict["in_successful_contract_call"]
        )
        event = ContractEvent.from_json_dict(json_dict["event"])
        return cls(
            in_successful_contract_call=in_successful_contract_call,
            event=event,
        )

    def __hash__(self):
        return hash(
            (
                self.in_successful_contract_call,
                self.event,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.in_successful_contract_call == other.in_successful_contract_call
            and self.event == other.event
        )

    def __repr__(self):
        out = [
            f"in_successful_contract_call={self.in_successful_contract_call}",
            f"event={self.event}",
        ]
        return f"<DiagnosticEvent [{', '.join(out)}]>"
