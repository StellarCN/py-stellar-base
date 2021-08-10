# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .account_id import AccountID

__all__ = ["LedgerKeyAccount"]


class LedgerKeyAccount:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct
        {
            AccountID accountID;
        }
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        account_id: AccountID,
    ) -> None:
        self.account_id = account_id

    def pack(self, packer: Packer) -> None:
        self.account_id.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerKeyAccount":
        account_id = AccountID.unpack(unpacker)
        return cls(
            account_id=account_id,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "LedgerKeyAccount":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerKeyAccount":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.account_id == other.account_id

    def __str__(self):
        out = [
            f"account_id={self.account_id}",
        ]
        return f"<LedgerKeyAccount {[', '.join(out)]}>"
