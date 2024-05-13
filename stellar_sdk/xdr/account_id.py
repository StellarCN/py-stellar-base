# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .public_key import PublicKey

__all__ = ["AccountID"]


class AccountID:
    """
    XDR Source Code::

        typedef PublicKey AccountID;
    """

    def __init__(self, account_id: PublicKey) -> None:
        self.account_id = account_id

    def pack(self, packer: Packer) -> None:
        self.account_id.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> AccountID:
        account_id = PublicKey.unpack(unpacker)
        return cls(account_id)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> AccountID:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> AccountID:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(self.account_id)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.account_id == other.account_id

    def __repr__(self):
        return f"<AccountID [account_id={self.account_id}]>"
