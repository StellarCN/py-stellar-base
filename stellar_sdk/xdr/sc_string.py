# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .base import String
from .constants import *

__all__ = ["SCString"]


class SCString:
    """
    XDR Source Code::

        typedef string SCString<SCVAL_LIMIT>;
    """

    def __init__(self, sc_string: bytes) -> None:
        self.sc_string = sc_string

    def pack(self, packer: Packer) -> None:
        String(self.sc_string, SCVAL_LIMIT).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCString":
        sc_string = String.unpack(unpacker)
        return cls(sc_string)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCString":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCString":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.sc_string == other.sc_string

    def __str__(self):
        return f"<SCString [sc_string={self.sc_string}]>"
