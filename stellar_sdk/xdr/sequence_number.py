# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .int64 import Int64

__all__ = ["SequenceNumber"]


class SequenceNumber:
    """
    XDR Source Code::

        typedef int64 SequenceNumber;
    """

    def __init__(self, sequence_number: Int64) -> None:
        self.sequence_number = sequence_number

    def pack(self, packer: Packer) -> None:
        self.sequence_number.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SequenceNumber:
        sequence_number = Int64.unpack(unpacker)
        return cls(sequence_number)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SequenceNumber:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SequenceNumber:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(self.sequence_number)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.sequence_number == other.sequence_number

    def __repr__(self):
        return f"<SequenceNumber [sequence_number={self.sequence_number}]>"
