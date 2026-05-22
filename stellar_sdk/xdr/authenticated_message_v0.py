# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> AuthenticatedMessageV0:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        sequence = Uint64.unpack(unpacker, depth_limit - 1)
        message = StellarMessage.unpack(unpacker, depth_limit - 1)
        mac = HmacSha256Mac.unpack(unpacker, depth_limit - 1)
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> AuthenticatedMessageV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> AuthenticatedMessageV0:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "sequence": self.sequence.to_json_dict(),
            "message": self.message.to_json_dict(),
            "mac": self.mac.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> AuthenticatedMessageV0:
        sequence = Uint64.from_json_dict(json_dict["sequence"])
        message = StellarMessage.from_json_dict(json_dict["message"])
        mac = HmacSha256Mac.from_json_dict(json_dict["mac"])
        return cls(
            sequence=sequence,
            message=message,
            mac=mac,
        )

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
