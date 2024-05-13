# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .sc_meta_kind import SCMetaKind
from .sc_meta_v0 import SCMetaV0

__all__ = ["SCMetaEntry"]


class SCMetaEntry:
    """
    XDR Source Code::

        union SCMetaEntry switch (SCMetaKind kind)
        {
        case SC_META_V0:
            SCMetaV0 v0;
        };
    """

    def __init__(
        self,
        kind: SCMetaKind,
        v0: SCMetaV0 = None,
    ) -> None:
        self.kind = kind
        self.v0 = v0

    def pack(self, packer: Packer) -> None:
        self.kind.pack(packer)
        if self.kind == SCMetaKind.SC_META_V0:
            if self.v0 is None:
                raise ValueError("v0 should not be None.")
            self.v0.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCMetaEntry:
        kind = SCMetaKind.unpack(unpacker)
        if kind == SCMetaKind.SC_META_V0:
            v0 = SCMetaV0.unpack(unpacker)
            return cls(kind=kind, v0=v0)
        return cls(kind=kind)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCMetaEntry:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCMetaEntry:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.kind,
                self.v0,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.kind == other.kind and self.v0 == other.v0

    def __repr__(self):
        out = []
        out.append(f"kind={self.kind}")
        out.append(f"v0={self.v0}") if self.v0 is not None else None
        return f"<SCMetaEntry [{', '.join(out)}]>"
