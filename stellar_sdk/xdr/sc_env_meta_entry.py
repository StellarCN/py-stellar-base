# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .sc_env_meta_kind import SCEnvMetaKind
from .uint64 import Uint64

__all__ = ["SCEnvMetaEntry"]


class SCEnvMetaEntry:
    """
    XDR Source Code::

        union SCEnvMetaEntry switch (SCEnvMetaKind kind)
        {
        case SC_ENV_META_KIND_INTERFACE_VERSION:
            uint64 interfaceVersion;
        };
    """

    def __init__(
        self,
        kind: SCEnvMetaKind,
        interface_version: Uint64 = None,
    ) -> None:
        self.kind = kind
        self.interface_version = interface_version

    def pack(self, packer: Packer) -> None:
        self.kind.pack(packer)
        if self.kind == SCEnvMetaKind.SC_ENV_META_KIND_INTERFACE_VERSION:
            if self.interface_version is None:
                raise ValueError("interface_version should not be None.")
            self.interface_version.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCEnvMetaEntry:
        kind = SCEnvMetaKind.unpack(unpacker)
        if kind == SCEnvMetaKind.SC_ENV_META_KIND_INTERFACE_VERSION:
            interface_version = Uint64.unpack(unpacker)
            return cls(kind=kind, interface_version=interface_version)
        return cls(kind=kind)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCEnvMetaEntry:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCEnvMetaEntry:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.kind,
                self.interface_version,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.kind == other.kind
            and self.interface_version == other.interface_version
        )

    def __repr__(self):
        out = []
        out.append(f"kind={self.kind}")
        (
            out.append(f"interface_version={self.interface_version}")
            if self.interface_version is not None
            else None
        )
        return f"<SCEnvMetaEntry [{', '.join(out)}]>"
