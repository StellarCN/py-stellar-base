# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib3 import Packer, Unpacker

from .diagnostic_event import DiagnosticEvent

__all__ = ["OperationDiagnosticEvents"]


class OperationDiagnosticEvents:
    """
    XDR Source Code::

        struct OperationDiagnosticEvents
        {
            DiagnosticEvent events<>;
        };
    """

    def __init__(
        self,
        events: List[DiagnosticEvent],
    ) -> None:
        _expect_max_length = 4294967295
        if events and len(events) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `events` should be {_expect_max_length}, but got {len(events)}."
            )
        self.events = events

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.events))
        for events_item in self.events:
            events_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "OperationDiagnosticEvents":
        length = unpacker.unpack_uint()
        events = []
        for _ in range(length):
            events.append(DiagnosticEvent.unpack(unpacker))
        return cls(
            events=events,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "OperationDiagnosticEvents":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "OperationDiagnosticEvents":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.events == other.events

    def __str__(self):
        out = [
            f"events={self.events}",
        ]
        return f"<OperationDiagnosticEvents [{', '.join(out)}]>"
