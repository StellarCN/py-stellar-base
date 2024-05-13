# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

from .contract_event import ContractEvent
from .diagnostic_event import DiagnosticEvent
from .sc_val import SCVal
from .soroban_transaction_meta_ext import SorobanTransactionMetaExt

__all__ = ["SorobanTransactionMeta"]


class SorobanTransactionMeta:
    """
    XDR Source Code::

        struct SorobanTransactionMeta
        {
            SorobanTransactionMetaExt ext;

            ContractEvent events<>;             // custom events populated by the
                                                // contracts themselves.
            SCVal returnValue;                  // return value of the host fn invocation

            // Diagnostics events that are not hashed.
            // This will contain all contract and diagnostic events. Even ones
            // that were emitted in a failed contract call.
            DiagnosticEvent diagnosticEvents<>;
        };
    """

    def __init__(
        self,
        ext: SorobanTransactionMetaExt,
        events: List[ContractEvent],
        return_value: SCVal,
        diagnostic_events: List[DiagnosticEvent],
    ) -> None:
        _expect_max_length = 4294967295
        if events and len(events) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `events` should be {_expect_max_length}, but got {len(events)}."
            )
        _expect_max_length = 4294967295
        if diagnostic_events and len(diagnostic_events) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `diagnostic_events` should be {_expect_max_length}, but got {len(diagnostic_events)}."
            )
        self.ext = ext
        self.events = events
        self.return_value = return_value
        self.diagnostic_events = diagnostic_events

    def pack(self, packer: Packer) -> None:
        self.ext.pack(packer)
        packer.pack_uint(len(self.events))
        for events_item in self.events:
            events_item.pack(packer)
        self.return_value.pack(packer)
        packer.pack_uint(len(self.diagnostic_events))
        for diagnostic_events_item in self.diagnostic_events:
            diagnostic_events_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SorobanTransactionMeta:
        ext = SorobanTransactionMetaExt.unpack(unpacker)
        length = unpacker.unpack_uint()
        events = []
        for _ in range(length):
            events.append(ContractEvent.unpack(unpacker))
        return_value = SCVal.unpack(unpacker)
        length = unpacker.unpack_uint()
        diagnostic_events = []
        for _ in range(length):
            diagnostic_events.append(DiagnosticEvent.unpack(unpacker))
        return cls(
            ext=ext,
            events=events,
            return_value=return_value,
            diagnostic_events=diagnostic_events,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SorobanTransactionMeta:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SorobanTransactionMeta:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.ext,
                self.events,
                self.return_value,
                self.diagnostic_events,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ext == other.ext
            and self.events == other.events
            and self.return_value == other.return_value
            and self.diagnostic_events == other.diagnostic_events
        )

    def __repr__(self):
        out = [
            f"ext={self.ext}",
            f"events={self.events}",
            f"return_value={self.return_value}",
            f"diagnostic_events={self.diagnostic_events}",
        ]
        return f"<SorobanTransactionMeta [{', '.join(out)}]>"
