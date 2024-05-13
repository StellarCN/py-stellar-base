# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .extension_point import ExtensionPoint
from .uint32 import Uint32

__all__ = ["ExtendFootprintTTLOp"]


class ExtendFootprintTTLOp:
    """
    XDR Source Code::

        struct ExtendFootprintTTLOp
        {
            ExtensionPoint ext;
            uint32 extendTo;
        };
    """

    def __init__(
        self,
        ext: ExtensionPoint,
        extend_to: Uint32,
    ) -> None:
        self.ext = ext
        self.extend_to = extend_to

    def pack(self, packer: Packer) -> None:
        self.ext.pack(packer)
        self.extend_to.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ExtendFootprintTTLOp:
        ext = ExtensionPoint.unpack(unpacker)
        extend_to = Uint32.unpack(unpacker)
        return cls(
            ext=ext,
            extend_to=extend_to,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ExtendFootprintTTLOp:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ExtendFootprintTTLOp:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.ext,
                self.extend_to,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.ext == other.ext and self.extend_to == other.extend_to

    def __repr__(self):
        out = [
            f"ext={self.ext}",
            f"extend_to={self.extend_to}",
        ]
        return f"<ExtendFootprintTTLOp [{', '.join(out)}]>"
