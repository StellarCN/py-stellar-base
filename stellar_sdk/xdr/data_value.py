# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .base import Opaque

__all__ = ["DataValue"]


class DataValue:
    """
    XDR Source Code::

        typedef opaque DataValue<64>;
    """

    def __init__(self, data_value: bytes) -> None:
        self.data_value = data_value

    def pack(self, packer: Packer) -> None:
        Opaque(self.data_value, 64, False).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> DataValue:
        data_value = Opaque.unpack(unpacker, 64, False)
        return cls(data_value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> DataValue:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> DataValue:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(self.data_value)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.data_value == other.data_value

    def __repr__(self):
        return f"<DataValue [data_value={self.data_value}]>"
