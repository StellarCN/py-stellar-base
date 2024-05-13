# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .hmac_sha256_mac import HmacSha256Mac
from .stellar_message import StellarMessage
from .uint64 import Uint64

__all__ = ["AuthenticatedMessageV0"]


class AuthenticatedMessageV0:
    """
    XDR Source Code::

        struct
            {
                uint64 sequence;
                StellarMessage message;
                HmacSha256Mac mac;
            }
    """

    def __init__(
        self,
        sequence: Uint64,
        message: StellarMessage,
        mac: HmacSha256Mac,
    ) -> None:
        self.sequence = sequence
        self.message = message
        self.mac = mac

    def pack(self, packer: Packer) -> None:
        self.sequence.pack(packer)
        self.message.pack(packer)
        self.mac.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> AuthenticatedMessageV0:
        sequence = Uint64.unpack(unpacker)
        message = StellarMessage.unpack(unpacker)
        mac = HmacSha256Mac.unpack(unpacker)
        return cls(
            sequence=sequence,
            message=message,
            mac=mac,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> AuthenticatedMessageV0:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> AuthenticatedMessageV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.sequence,
                self.message,
                self.mac,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.sequence == other.sequence
            and self.message == other.message
            and self.mac == other.mac
        )

    def __repr__(self):
        out = [
            f"sequence={self.sequence}",
            f"message={self.message}",
            f"mac={self.mac}",
        ]
        return f"<AuthenticatedMessageV0 [{', '.join(out)}]>"
