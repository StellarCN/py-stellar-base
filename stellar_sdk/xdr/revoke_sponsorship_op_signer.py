# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .account_id import AccountID
from .signer_key import SignerKey

__all__ = ["RevokeSponsorshipOpSigner"]


class RevokeSponsorshipOpSigner:
    """
    XDR Source Code::

        struct
            {
                AccountID accountID;
                SignerKey signerKey;
            }
    """

    def __init__(
        self,
        account_id: AccountID,
        signer_key: SignerKey,
    ) -> None:
        self.account_id = account_id
        self.signer_key = signer_key

    def pack(self, packer: Packer) -> None:
        self.account_id.pack(packer)
        self.signer_key.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> RevokeSponsorshipOpSigner:
        account_id = AccountID.unpack(unpacker)
        signer_key = SignerKey.unpack(unpacker)
        return cls(
            account_id=account_id,
            signer_key=signer_key,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> RevokeSponsorshipOpSigner:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> RevokeSponsorshipOpSigner:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.account_id,
                self.signer_key,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.account_id == other.account_id and self.signer_key == other.signer_key
        )

    def __repr__(self):
        out = [
            f"account_id={self.account_id}",
            f"signer_key={self.signer_key}",
        ]
        return f"<RevokeSponsorshipOpSigner [{', '.join(out)}]>"
