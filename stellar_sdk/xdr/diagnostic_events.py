# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

from .diagnostic_event import DiagnosticEvent

__all__ = ["DiagnosticEvents"]


class DiagnosticEvents:
    """
    XDR Source Code::

        typedef DiagnosticEvent DiagnosticEvents<>;
    """

    def __init__(self, diagnostic_events: List[DiagnosticEvent]) -> None:
        _expect_max_length = 4294967295
        if diagnostic_events and len(diagnostic_events) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `diagnostic_events` should be {_expect_max_length}, but got {len(diagnostic_events)}."
            )
        self.diagnostic_events = diagnostic_events

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.diagnostic_events))
        for diagnostic_events_item in self.diagnostic_events:
            diagnostic_events_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> DiagnosticEvents:
        length = unpacker.unpack_uint()
        diagnostic_events = []
        for _ in range(length):
            diagnostic_events.append(DiagnosticEvent.unpack(unpacker))
        return cls(diagnostic_events)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> DiagnosticEvents:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> DiagnosticEvents:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(self.diagnostic_events)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.diagnostic_events == other.diagnostic_events

    def __repr__(self):
        return f"<DiagnosticEvents [diagnostic_events={self.diagnostic_events}]>"
