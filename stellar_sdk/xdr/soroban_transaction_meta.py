# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SorobanTransactionMeta:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        ext = SorobanTransactionMetaExt.unpack(unpacker, depth_limit - 1)
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"events length {length} exceeds remaining input length {_remaining}"
            )
        events = []
        for _ in range(length):
            events.append(ContractEvent.unpack(unpacker, depth_limit - 1))
        return_value = SCVal.unpack(unpacker, depth_limit - 1)
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"diagnostic_events length {length} exceeds remaining input length {_remaining}"
            )
        diagnostic_events = []
        for _ in range(length):
            diagnostic_events.append(DiagnosticEvent.unpack(unpacker, depth_limit - 1))
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SorobanTransactionMeta:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SorobanTransactionMeta:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "ext": self.ext.to_json_dict(),
            "events": [item.to_json_dict() for item in self.events],
            "return_value": self.return_value.to_json_dict(),
            "diagnostic_events": [
                item.to_json_dict() for item in self.diagnostic_events
            ],
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SorobanTransactionMeta:
        ext = SorobanTransactionMetaExt.from_json_dict(json_dict["ext"])
        events = [ContractEvent.from_json_dict(item) for item in json_dict["events"]]
        return_value = SCVal.from_json_dict(json_dict["return_value"])
        diagnostic_events = [
            DiagnosticEvent.from_json_dict(item)
            for item in json_dict["diagnostic_events"]
        ]
        return cls(
            ext=ext,
            events=events,
            return_value=return_value,
            diagnostic_events=diagnostic_events,
        )

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
