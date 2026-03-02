# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> InvokeHostFunctionSuccessPreImage:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        return_value = SCVal.unpack(unpacker, depth_limit - 1)
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"events length {length} exceeds remaining input length {_remaining}"
            )
        events = []
        for _ in range(length):
            events.append(ContractEvent.unpack(unpacker, depth_limit - 1))
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> InvokeHostFunctionSuccessPreImage:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> InvokeHostFunctionSuccessPreImage:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "return_value": self.return_value.to_json_dict(),
            "events": [item.to_json_dict() for item in self.events],
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> InvokeHostFunctionSuccessPreImage:
        return_value = SCVal.from_json_dict(json_dict["return_value"])
        events = [ContractEvent.from_json_dict(item) for item in json_dict["events"]]
        return cls(
            return_value=return_value,
            events=events,
        )

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
