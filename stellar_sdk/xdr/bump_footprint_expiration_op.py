# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .extension_point import ExtensionPoint
from .uint32 import Uint32

__all__ = ["BumpFootprintExpirationOp"]


class BumpFootprintExpirationOp:
    """
    XDR Source Code::

        struct BumpFootprintExpirationOp
        {
            ExtensionPoint ext;
            uint32 ledgersToExpire;
        };
    """

    def __init__(
        self,
        ext: ExtensionPoint,
        ledgers_to_expire: Uint32,
    ) -> None:
        self.ext = ext
        self.ledgers_to_expire = ledgers_to_expire

    def pack(self, packer: Packer) -> None:
        self.ext.pack(packer)
        self.ledgers_to_expire.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> BumpFootprintExpirationOp:
        ext = ExtensionPoint.unpack(unpacker)
        ledgers_to_expire = Uint32.unpack(unpacker)
        return cls(
            ext=ext,
            ledgers_to_expire=ledgers_to_expire,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> BumpFootprintExpirationOp:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> BumpFootprintExpirationOp:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.ext,
                self.ledgers_to_expire,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ext == other.ext and self.ledgers_to_expire == other.ledgers_to_expire
        )

    def __str__(self):
        out = [
            f"ext={self.ext}",
            f"ledgers_to_expire={self.ledgers_to_expire}",
        ]
        return f"<BumpFootprintExpirationOp [{', '.join(out)}]>"
