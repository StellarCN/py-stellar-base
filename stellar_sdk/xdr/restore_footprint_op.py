# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .extension_point import ExtensionPoint

__all__ = ["RestoreFootprintOp"]


class RestoreFootprintOp:
    """
    XDR Source Code::

        struct RestoreFootprintOp
        {
            ExtensionPoint ext;
        };
    """

    def __init__(
        self,
        ext: ExtensionPoint,
    ) -> None:
        self.ext = ext

    def pack(self, packer: Packer) -> None:
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> RestoreFootprintOp:
        ext = ExtensionPoint.unpack(unpacker)
        return cls(
            ext=ext,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> RestoreFootprintOp:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> RestoreFootprintOp:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash((self.ext,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.ext == other.ext

    def __repr__(self):
        out = [
            f"ext={self.ext}",
        ]
        return f"<RestoreFootprintOp [{', '.join(out)}]>"
