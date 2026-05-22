# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .message_type import MessageType
from .uint256 import Uint256

__all__ = ["DontHave"]


class DontHave:
    """
    XDR Source Code::

        struct DontHave
        {
            MessageType type;
            uint256 reqHash;
        };
    """

    def __init__(
        self,
        type: MessageType,
        req_hash: Uint256,
    ) -> None:
        self.type = type
        self.req_hash = req_hash

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        self.req_hash.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> DontHave:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = MessageType.unpack(unpacker)
        req_hash = Uint256.unpack(unpacker, depth_limit - 1)
        return cls(
            type=type,
            req_hash=req_hash,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> DontHave:
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
    def from_xdr(cls, xdr: str) -> DontHave:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> DontHave:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "type": self.type.to_json_dict(),
            "req_hash": self.req_hash.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> DontHave:
        type = MessageType.from_json_dict(json_dict["type"])
        req_hash = Uint256.from_json_dict(json_dict["req_hash"])
        return cls(
            type=type,
            req_hash=req_hash,
        )

    def __hash__(self):
        return hash(
            (
                self.type,
                self.req_hash,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.type == other.type and self.req_hash == other.req_hash

    def __repr__(self):
        out = [
            f"type={self.type}",
            f"req_hash={self.req_hash}",
        ]
        return f"<DontHave [{', '.join(out)}]>"
