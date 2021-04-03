# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib import Packer, Unpacker

from .account_entry_extension_v2_ext import AccountEntryExtensionV2Ext
from .constants import *
from .sponsorship_descriptor import SponsorshipDescriptor
from .uint32 import Uint32
from ..exceptions import ValueError

__all__ = ["AccountEntryExtensionV2"]


class AccountEntryExtensionV2:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct AccountEntryExtensionV2
    {
        uint32 numSponsored;
        uint32 numSponsoring;
        SponsorshipDescriptor signerSponsoringIDs<MAX_SIGNERS>;

        union switch (int v)
        {
        case 0:
            void;
        }
        ext;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        num_sponsored: Uint32,
        num_sponsoring: Uint32,
        signer_sponsoring_i_ds: List[SponsorshipDescriptor],
        ext: AccountEntryExtensionV2Ext,
    ) -> None:
        if signer_sponsoring_i_ds and len(signer_sponsoring_i_ds) > MAX_SIGNERS:
            raise ValueError(
                f"The maximum length of `signer_sponsoring_i_ds` should be MAX_SIGNERS, but got {len(signer_sponsoring_i_ds)}."
            )
        self.num_sponsored = num_sponsored
        self.num_sponsoring = num_sponsoring
        self.signer_sponsoring_i_ds = signer_sponsoring_i_ds
        self.ext = ext

    def pack(self, packer: Packer) -> None:
        self.num_sponsored.pack(packer)
        self.num_sponsoring.pack(packer)
        packer.pack_uint(len(self.signer_sponsoring_i_ds))
        for signer_sponsoring_i_d in self.signer_sponsoring_i_ds:
            signer_sponsoring_i_d.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AccountEntryExtensionV2":
        num_sponsored = Uint32.unpack(unpacker)
        num_sponsoring = Uint32.unpack(unpacker)
        length = unpacker.unpack_uint()
        signer_sponsoring_i_ds = []
        for _ in range(length):
            signer_sponsoring_i_ds.append(SponsorshipDescriptor.unpack(unpacker))
        ext = AccountEntryExtensionV2Ext.unpack(unpacker)
        return cls(
            num_sponsored=num_sponsored,
            num_sponsoring=num_sponsoring,
            signer_sponsoring_i_ds=signer_sponsoring_i_ds,
            ext=ext,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "AccountEntryExtensionV2":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AccountEntryExtensionV2":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.num_sponsored == other.num_sponsored
            and self.num_sponsoring == other.num_sponsoring
            and self.signer_sponsoring_i_ds == other.signer_sponsoring_i_ds
            and self.ext == other.ext
        )

    def __str__(self):
        out = [
            f"num_sponsored={self.num_sponsored}",
            f"num_sponsoring={self.num_sponsoring}",
            f"signer_sponsoring_i_ds={self.signer_sponsoring_i_ds}",
            f"ext={self.ext}",
        ]
        return f"<AccountEntryExtensionV2 {[', '.join(out)]}>"
