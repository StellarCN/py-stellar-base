# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .sequence_number import SequenceNumber

__all__ = ["BumpSequenceOp"]


class BumpSequenceOp:
    """
    XDR Source Code::

        struct BumpSequenceOp
        {
            SequenceNumber bumpTo;
        };
    """

    def __init__(
        self,
        bump_to: SequenceNumber,
    ) -> None:
        self.bump_to = bump_to

    def pack(self, packer: Packer) -> None:
        self.bump_to.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> BumpSequenceOp:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        bump_to = SequenceNumber.unpack(unpacker, depth_limit - 1)
        return cls(
            bump_to=bump_to,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> BumpSequenceOp:
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
    def from_xdr(cls, xdr: str) -> BumpSequenceOp:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> BumpSequenceOp:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "bump_to": self.bump_to.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> BumpSequenceOp:
        bump_to = SequenceNumber.from_json_dict(json_dict["bump_to"])
        return cls(
            bump_to=bump_to,
        )

    def __hash__(self):
        return hash((self.bump_to,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.bump_to == other.bump_to

    def __repr__(self):
        out = [
            f"bump_to={self.bump_to}",
        ]
        return f"<BumpSequenceOp [{', '.join(out)}]>"
