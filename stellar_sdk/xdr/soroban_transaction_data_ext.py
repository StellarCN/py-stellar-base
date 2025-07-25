# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import Integer
from .soroban_resources_ext_v0 import SorobanResourcesExtV0

__all__ = ["SorobanTransactionDataExt"]


class SorobanTransactionDataExt:
    """
    XDR Source Code::

        union switch (int v)
            {
            case 0:
                void;
            case 1:
                SorobanResourcesExtV0 resourceExt;
            }
    """

    def __init__(
        self,
        v: int,
        resource_ext: Optional[SorobanResourcesExtV0] = None,
    ) -> None:
        self.v = v
        self.resource_ext = resource_ext

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            return
        if self.v == 1:
            if self.resource_ext is None:
                raise ValueError("resource_ext should not be None.")
            self.resource_ext.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SorobanTransactionDataExt:
        v = Integer.unpack(unpacker)
        if v == 0:
            return cls(v=v)
        if v == 1:
            resource_ext = SorobanResourcesExtV0.unpack(unpacker)
            return cls(v=v, resource_ext=resource_ext)
        return cls(v=v)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SorobanTransactionDataExt:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SorobanTransactionDataExt:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.v,
                self.resource_ext,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v and self.resource_ext == other.resource_ext

    def __repr__(self):
        out = []
        out.append(f"v={self.v}")
        (
            out.append(f"resource_ext={self.resource_ext}")
            if self.resource_ext is not None
            else None
        )
        return f"<SorobanTransactionDataExt [{', '.join(out)}]>"
