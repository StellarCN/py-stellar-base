# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .account_id import AccountID
from .uint256 import Uint256

__all__ = ["HashIDPreimageSourceContractID"]


class HashIDPreimageSourceContractID:
    """
    XDR Source Code::

        struct
            {
                AccountID sourceAccount;
                uint256 salt;
            }
    """

    def __init__(
        self,
        source_account: AccountID,
        salt: Uint256,
    ) -> None:
        self.source_account = source_account
        self.salt = salt

    def pack(self, packer: Packer) -> None:
        self.source_account.pack(packer)
        self.salt.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "HashIDPreimageSourceContractID":
        source_account = AccountID.unpack(unpacker)
        salt = Uint256.unpack(unpacker)
        return cls(
            source_account=source_account,
            salt=salt,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "HashIDPreimageSourceContractID":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "HashIDPreimageSourceContractID":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.source_account == other.source_account and self.salt == other.salt

    def __str__(self):
        out = [
            f"source_account={self.source_account}",
            f"salt={self.salt}",
        ]
        return f"<HashIDPreimageSourceContractID [{', '.join(out)}]>"
