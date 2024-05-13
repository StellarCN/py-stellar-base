# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

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
    def unpack(cls, unpacker: Unpacker) -> Liabilities:
        buying = Int64.unpack(unpacker)
        selling = Int64.unpack(unpacker)
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
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> Liabilities:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
