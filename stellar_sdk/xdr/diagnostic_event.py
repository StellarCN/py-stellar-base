# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .base import Boolean
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
    def unpack(cls, unpacker: Unpacker) -> DiagnosticEvent:
        in_successful_contract_call = Boolean.unpack(unpacker)
        event = ContractEvent.unpack(unpacker)
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
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> DiagnosticEvent:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
