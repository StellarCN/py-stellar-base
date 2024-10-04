# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .uint32 import Uint32

__all__ = ["SCEnvMetaEntryInterfaceVersion"]


class SCEnvMetaEntryInterfaceVersion:
    """
    XDR Source Code::

        struct {
                uint32 protocol;
                uint32 preRelease;
            }
    """

    def __init__(
        self,
        protocol: Uint32,
        pre_release: Uint32,
    ) -> None:
        self.protocol = protocol
        self.pre_release = pre_release

    def pack(self, packer: Packer) -> None:
        self.protocol.pack(packer)
        self.pre_release.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCEnvMetaEntryInterfaceVersion:
        protocol = Uint32.unpack(unpacker)
        pre_release = Uint32.unpack(unpacker)
        return cls(
            protocol=protocol,
            pre_release=pre_release,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCEnvMetaEntryInterfaceVersion:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCEnvMetaEntryInterfaceVersion:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.protocol,
                self.pre_release,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.protocol == other.protocol and self.pre_release == other.pre_release

    def __repr__(self):
        out = [
            f"protocol={self.protocol}",
            f"pre_release={self.pre_release}",
        ]
        return f"<SCEnvMetaEntryInterfaceVersion [{', '.join(out)}]>"
