# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List, Optional
from xdrlib import Packer, Unpacker

from .account_entry_ext import AccountEntryExt
from .account_id import AccountID
from .constants import *
from .int64 import Int64
from .sequence_number import SequenceNumber
from .signer import Signer
from .string32 import String32
from .thresholds import Thresholds
from .uint32 import Uint32
from ..exceptions import ValueError

__all__ = ["AccountEntry"]


class AccountEntry:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct AccountEntry
    {
        AccountID accountID;      // master public key for this account
        int64 balance;            // in stroops
        SequenceNumber seqNum;    // last sequence number used for this account
        uint32 numSubEntries;     // number of sub-entries this account has
                                  // drives the reserve
        AccountID* inflationDest; // Account to vote for during inflation
        uint32 flags;             // see AccountFlags

        string32 homeDomain; // can be used for reverse federation and memo lookup

        // fields used for signatures
        // thresholds stores unsigned bytes: [weight of master|low|medium|high]
        Thresholds thresholds;

        Signer signers<MAX_SIGNERS>; // possible signers for this account

        // reserved for future use
        union switch (int v)
        {
        case 0:
            void;
        case 1:
            AccountEntryExtensionV1 v1;
        }
        ext;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        account_id: AccountID,
        balance: Int64,
        seq_num: SequenceNumber,
        num_sub_entries: Uint32,
        inflation_dest: Optional[AccountID],
        flags: Uint32,
        home_domain: String32,
        thresholds: Thresholds,
        signers: List[Signer],
        ext: AccountEntryExt,
    ) -> None:
        if signers and len(signers) > MAX_SIGNERS:
            raise ValueError(
                f"The maximum length of `signers` should be MAX_SIGNERS, but got {len(signers)}."
            )
        self.account_id = account_id
        self.balance = balance
        self.seq_num = seq_num
        self.num_sub_entries = num_sub_entries
        self.inflation_dest = inflation_dest
        self.flags = flags
        self.home_domain = home_domain
        self.thresholds = thresholds
        self.signers = signers
        self.ext = ext

    def pack(self, packer: Packer) -> None:
        self.account_id.pack(packer)
        self.balance.pack(packer)
        self.seq_num.pack(packer)
        self.num_sub_entries.pack(packer)
        if self.inflation_dest is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.inflation_dest.pack(packer)
        self.flags.pack(packer)
        self.home_domain.pack(packer)
        self.thresholds.pack(packer)
        packer.pack_uint(len(self.signers))
        for signer in self.signers:
            signer.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AccountEntry":
        account_id = AccountID.unpack(unpacker)
        balance = Int64.unpack(unpacker)
        seq_num = SequenceNumber.unpack(unpacker)
        num_sub_entries = Uint32.unpack(unpacker)
        inflation_dest = AccountID.unpack(unpacker) if unpacker.unpack_uint() else None
        flags = Uint32.unpack(unpacker)
        home_domain = String32.unpack(unpacker)
        thresholds = Thresholds.unpack(unpacker)
        length = unpacker.unpack_uint()
        signers = []
        for _ in range(length):
            signers.append(Signer.unpack(unpacker))
        ext = AccountEntryExt.unpack(unpacker)
        return cls(
            account_id=account_id,
            balance=balance,
            seq_num=seq_num,
            num_sub_entries=num_sub_entries,
            inflation_dest=inflation_dest,
            flags=flags,
            home_domain=home_domain,
            thresholds=thresholds,
            signers=signers,
            ext=ext,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "AccountEntry":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AccountEntry":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.account_id == other.account_id
            and self.balance == other.balance
            and self.seq_num == other.seq_num
            and self.num_sub_entries == other.num_sub_entries
            and self.inflation_dest == other.inflation_dest
            and self.flags == other.flags
            and self.home_domain == other.home_domain
            and self.thresholds == other.thresholds
            and self.signers == other.signers
            and self.ext == other.ext
        )

    def __str__(self):
        out = [
            f"account_id={self.account_id}",
            f"balance={self.balance}",
            f"seq_num={self.seq_num}",
            f"num_sub_entries={self.num_sub_entries}",
            f"inflation_dest={self.inflation_dest}",
            f"flags={self.flags}",
            f"home_domain={self.home_domain}",
            f"thresholds={self.thresholds}",
            f"signers={self.signers}",
            f"ext={self.ext}",
        ]
        return f"<AccountEntry {[', '.join(out)]}>"
