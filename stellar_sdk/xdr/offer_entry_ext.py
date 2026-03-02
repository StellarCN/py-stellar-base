# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, Integer

__all__ = ["OfferEntryExt"]


class OfferEntryExt:
    """
    XDR Source Code::

        union switch (int v)
            {
            case 0:
                void;
            }
    """

    def __init__(
        self,
        v: int,
    ) -> None:
        self.v = v

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            return
        raise ValueError("Invalid v.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> OfferEntryExt:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        v = Integer.unpack(unpacker)
        if v == 0:
            return cls(v=v)
        raise ValueError("Invalid v.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> OfferEntryExt:
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
    def from_xdr(cls, xdr: str) -> OfferEntryExt:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> OfferEntryExt:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.v == 0:
            return "v0"
        raise ValueError(f"Unknown v in OfferEntryExt: {self.v}")

    @classmethod
    def from_json_dict(cls, json_value: str) -> OfferEntryExt:
        if json_value not in ("v0",):
            raise ValueError(
                f"Unexpected string '{json_value}' for OfferEntryExt, must be one of: v0"
            )
        v = int(json_value[1:])
        return cls(v=v)

    def __hash__(self):
        return hash((self.v,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v

    def __repr__(self):
        out = []
        out.append(f"v={self.v}")
        return f"<OfferEntryExt [{', '.join(out)}]>"
