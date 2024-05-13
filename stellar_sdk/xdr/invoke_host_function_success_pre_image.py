# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

from .contract_event import ContractEvent
from .sc_val import SCVal

__all__ = ["InvokeHostFunctionSuccessPreImage"]


class InvokeHostFunctionSuccessPreImage:
    """
    XDR Source Code::

        struct InvokeHostFunctionSuccessPreImage
        {
            SCVal returnValue;
            ContractEvent events<>;
        };
    """

    def __init__(
        self,
        return_value: SCVal,
        events: List[ContractEvent],
    ) -> None:
        _expect_max_length = 4294967295
        if events and len(events) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `events` should be {_expect_max_length}, but got {len(events)}."
            )
        self.return_value = return_value
        self.events = events

    def pack(self, packer: Packer) -> None:
        self.return_value.pack(packer)
        packer.pack_uint(len(self.events))
        for events_item in self.events:
            events_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> InvokeHostFunctionSuccessPreImage:
        return_value = SCVal.unpack(unpacker)
        length = unpacker.unpack_uint()
        events = []
        for _ in range(length):
            events.append(ContractEvent.unpack(unpacker))
        return cls(
            return_value=return_value,
            events=events,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> InvokeHostFunctionSuccessPreImage:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> InvokeHostFunctionSuccessPreImage:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.return_value,
                self.events,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.return_value == other.return_value and self.events == other.events

    def __repr__(self):
        out = [
            f"return_value={self.return_value}",
            f"events={self.events}",
        ]
        return f"<InvokeHostFunctionSuccessPreImage [{', '.join(out)}]>"
