# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .uint64 import Uint64
from .uint256 import Uint256

__all__ = ["MuxedAccountMed25519"]


class MuxedAccountMed25519:
    """
    XDR Source Code::

        struct
            {
                uint64 id;
                uint256 ed25519;
            }
    """

    def __init__(
        self,
        id: Uint64,
        ed25519: Uint256,
    ) -> None:
        self.id = id
        self.ed25519 = ed25519

    def pack(self, packer: Packer) -> None:
        self.id.pack(packer)
        self.ed25519.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> MuxedAccountMed25519:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        id = Uint64.unpack(unpacker, depth_limit - 1)
        ed25519 = Uint256.unpack(unpacker, depth_limit - 1)
        return cls(
            id=id,
            ed25519=ed25519,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> MuxedAccountMed25519:
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
    def from_xdr(cls, xdr: str) -> MuxedAccountMed25519:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> MuxedAccountMed25519:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "id": self.id.to_json_dict(),
            "ed25519": self.ed25519.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> MuxedAccountMed25519:
        id = Uint64.from_json_dict(json_dict["id"])
        ed25519 = Uint256.from_json_dict(json_dict["ed25519"])
        return cls(
            id=id,
            ed25519=ed25519,
        )

    def __hash__(self):
        return hash(
            (
                self.id,
                self.ed25519,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.id == other.id and self.ed25519 == other.ed25519

    def __repr__(self):
        out = [
            f"id={self.id}",
            f"ed25519={self.ed25519}",
        ]
        return f"<MuxedAccountMed25519 [{', '.join(out)}]>"
