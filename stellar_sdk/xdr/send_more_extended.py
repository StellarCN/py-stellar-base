# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .uint32 import Uint32

__all__ = ["SendMoreExtended"]


class SendMoreExtended:
    """
    XDR Source Code::

        struct SendMoreExtended
        {
            uint32 numMessages;
            uint32 numBytes;
        };
    """

    def __init__(
        self,
        num_messages: Uint32,
        num_bytes: Uint32,
    ) -> None:
        self.num_messages = num_messages
        self.num_bytes = num_bytes

    def pack(self, packer: Packer) -> None:
        self.num_messages.pack(packer)
        self.num_bytes.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SendMoreExtended:
        num_messages = Uint32.unpack(unpacker)
        num_bytes = Uint32.unpack(unpacker)
        return cls(
            num_messages=num_messages,
            num_bytes=num_bytes,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SendMoreExtended:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SendMoreExtended:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.num_messages,
                self.num_bytes,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.num_messages == other.num_messages
            and self.num_bytes == other.num_bytes
        )

    def __repr__(self):
        out = [
            f"num_messages={self.num_messages}",
            f"num_bytes={self.num_bytes}",
        ]
        return f"<SendMoreExtended [{', '.join(out)}]>"
