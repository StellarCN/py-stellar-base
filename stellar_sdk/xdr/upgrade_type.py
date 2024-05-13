# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .base import Opaque

__all__ = ["UpgradeType"]


class UpgradeType:
    """
    XDR Source Code::

        typedef opaque UpgradeType<128>;
    """

    def __init__(self, upgrade_type: bytes) -> None:
        self.upgrade_type = upgrade_type

    def pack(self, packer: Packer) -> None:
        Opaque(self.upgrade_type, 128, False).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> UpgradeType:
        upgrade_type = Opaque.unpack(unpacker, 128, False)
        return cls(upgrade_type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> UpgradeType:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> UpgradeType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(self.upgrade_type)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.upgrade_type == other.upgrade_type

    def __repr__(self):
        return f"<UpgradeType [upgrade_type={self.upgrade_type}]>"
