# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .account_id import AccountID
from .string64 import String64

__all__ = ["LedgerKeyData"]


class LedgerKeyData:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct
        {
            AccountID accountID;
            string64 dataName;
        }
    ----------------------------------------------------------------
    """

    def __init__(self, account_id: AccountID, data_name: String64,) -> None:
        self.account_id = account_id
        self.data_name = data_name

    def pack(self, packer: Packer) -> None:
        self.account_id.pack(packer)
        self.data_name.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerKeyData":
        account_id = AccountID.unpack(unpacker)
        data_name = String64.unpack(unpacker)
        return cls(account_id=account_id, data_name=data_name,)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "LedgerKeyData":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerKeyData":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.account_id == other.account_id and self.data_name == other.data_name

    def __str__(self):
        out = [
            f"account_id={self.account_id}",
            f"data_name={self.data_name}",
        ]
        return f"<LedgerKeyData {[', '.join(out)]}>"
