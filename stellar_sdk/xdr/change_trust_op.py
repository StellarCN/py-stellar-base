# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .change_trust_asset import ChangeTrustAsset
from .int64 import Int64

__all__ = ["ChangeTrustOp"]


class ChangeTrustOp:
    """
    XDR Source Code::

        struct ChangeTrustOp
        {
            ChangeTrustAsset line;

            // if limit is set to 0, deletes the trust line
            int64 limit;
        };
    """

    def __init__(
        self,
        line: ChangeTrustAsset,
        limit: Int64,
    ) -> None:
        self.line = line
        self.limit = limit

    def pack(self, packer: Packer) -> None:
        self.line.pack(packer)
        self.limit.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ChangeTrustOp:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        line = ChangeTrustAsset.unpack(unpacker, depth_limit - 1)
        limit = Int64.unpack(unpacker, depth_limit - 1)
        return cls(
            line=line,
            limit=limit,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ChangeTrustOp:
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
    def from_xdr(cls, xdr: str) -> ChangeTrustOp:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ChangeTrustOp:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "line": self.line.to_json_dict(),
            "limit": self.limit.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> ChangeTrustOp:
        line = ChangeTrustAsset.from_json_dict(json_dict["line"])
        limit = Int64.from_json_dict(json_dict["limit"])
        return cls(
            line=line,
            limit=limit,
        )

    def __hash__(self):
        return hash(
            (
                self.line,
                self.limit,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.line == other.line and self.limit == other.limit

    def __repr__(self):
        out = [
            f"line={self.line}",
            f"limit={self.limit}",
        ]
        return f"<ChangeTrustOp [{', '.join(out)}]>"
