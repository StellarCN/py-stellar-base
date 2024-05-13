# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .account_entry_extension_v3 import AccountEntryExtensionV3
from .base import Integer

__all__ = ["AccountEntryExtensionV2Ext"]


class AccountEntryExtensionV2Ext:
    """
    XDR Source Code::

        union switch (int v)
            {
            case 0:
                void;
            case 3:
                AccountEntryExtensionV3 v3;
            }
    """

    def __init__(
        self,
        v: int,
        v3: AccountEntryExtensionV3 = None,
    ) -> None:
        self.v = v
        self.v3 = v3

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            return
        if self.v == 3:
            if self.v3 is None:
                raise ValueError("v3 should not be None.")
            self.v3.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> AccountEntryExtensionV2Ext:
        v = Integer.unpack(unpacker)
        if v == 0:
            return cls(v=v)
        if v == 3:
            v3 = AccountEntryExtensionV3.unpack(unpacker)
            return cls(v=v, v3=v3)
        return cls(v=v)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> AccountEntryExtensionV2Ext:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> AccountEntryExtensionV2Ext:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.v,
                self.v3,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v and self.v3 == other.v3

    def __repr__(self):
        out = []
        out.append(f"v={self.v}")
        out.append(f"v3={self.v3}") if self.v3 is not None else None
        return f"<AccountEntryExtensionV2Ext [{', '.join(out)}]>"
