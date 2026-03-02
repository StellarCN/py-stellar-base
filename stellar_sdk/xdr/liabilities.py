# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .int64 import Int64

__all__ = ["Liabilities"]


class Liabilities:
    """
    XDR Source Code::

        struct Liabilities
        {
            int64 buying;
            int64 selling;
        };
    """

    def __init__(
        self,
        buying: Int64,
        selling: Int64,
    ) -> None:
        self.buying = buying
        self.selling = selling

    def pack(self, packer: Packer) -> None:
        self.buying.pack(packer)
        self.selling.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> Liabilities:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        buying = Int64.unpack(unpacker, depth_limit - 1)
        selling = Int64.unpack(unpacker, depth_limit - 1)
        return cls(
            buying=buying,
            selling=selling,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Liabilities:
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
    def from_xdr(cls, xdr: str) -> Liabilities:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Liabilities:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "buying": self.buying.to_json_dict(),
            "selling": self.selling.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> Liabilities:
        buying = Int64.from_json_dict(json_dict["buying"])
        selling = Int64.from_json_dict(json_dict["selling"])
        return cls(
            buying=buying,
            selling=selling,
        )

    def __hash__(self):
        return hash(
            (
                self.buying,
                self.selling,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.buying == other.buying and self.selling == other.selling

    def __repr__(self):
        out = [
            f"buying={self.buying}",
            f"selling={self.selling}",
        ]
        return f"<Liabilities [{', '.join(out)}]>"
