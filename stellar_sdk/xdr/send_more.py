# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .uint32 import Uint32

__all__ = ["SendMore"]


class SendMore:
    """
    XDR Source Code::

        struct SendMore
        {
            uint32 numMessages;
        };
    """

    def __init__(
        self,
        num_messages: Uint32,
    ) -> None:
        self.num_messages = num_messages

    def pack(self, packer: Packer) -> None:
        self.num_messages.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SendMore:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        num_messages = Uint32.unpack(unpacker, depth_limit - 1)
        return cls(
            num_messages=num_messages,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SendMore:
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
    def from_xdr(cls, xdr: str) -> SendMore:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SendMore:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "num_messages": self.num_messages.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SendMore:
        num_messages = Uint32.from_json_dict(json_dict["num_messages"])
        return cls(
            num_messages=num_messages,
        )

    def __hash__(self):
        return hash((self.num_messages,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.num_messages == other.num_messages

    def __repr__(self):
        out = [
            f"num_messages={self.num_messages}",
        ]
        return f"<SendMore [{', '.join(out)}]>"
