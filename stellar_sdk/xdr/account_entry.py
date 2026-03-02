# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List, Optional

from xdrlib3 import Packer, Unpacker

from .account_entry_ext import AccountEntryExt
from .account_id import AccountID
from .base import DEFAULT_XDR_MAX_DEPTH
from .constants import *
from .int64 import Int64
from .sequence_number import SequenceNumber
from .signer import Signer
from .string32 import String32
from .thresholds import Thresholds
from .uint32 import Uint32

__all__ = ["AccountEntry"]


class AccountEntry:
    """
    XDR Source Code::

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
        _expect_max_length = MAX_SIGNERS
        if signers and len(signers) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `signers` should be {_expect_max_length}, but got {len(signers)}."
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
        for signers_item in self.signers:
            signers_item.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> AccountEntry:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        account_id = AccountID.unpack(unpacker, depth_limit - 1)
        balance = Int64.unpack(unpacker, depth_limit - 1)
        seq_num = SequenceNumber.unpack(unpacker, depth_limit - 1)
        num_sub_entries = Uint32.unpack(unpacker, depth_limit - 1)
        inflation_dest = (
            AccountID.unpack(unpacker, depth_limit - 1)
            if unpacker.unpack_uint()
            else None
        )
        flags = Uint32.unpack(unpacker, depth_limit - 1)
        home_domain = String32.unpack(unpacker, depth_limit - 1)
        thresholds = Thresholds.unpack(unpacker, depth_limit - 1)
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"signers length {length} exceeds remaining input length {_remaining}"
            )
        signers = []
        for _ in range(length):
            signers.append(Signer.unpack(unpacker, depth_limit - 1))
        ext = AccountEntryExt.unpack(unpacker, depth_limit - 1)
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
    def from_xdr_bytes(cls, xdr: bytes) -> AccountEntry:
        unpacker = Unpacker(xdr)
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> AccountEntry:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> AccountEntry:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "account_id": self.account_id.to_json_dict(),
            "balance": self.balance.to_json_dict(),
            "seq_num": self.seq_num.to_json_dict(),
            "num_sub_entries": self.num_sub_entries.to_json_dict(),
            "inflation_dest": (
                self.inflation_dest.to_json_dict()
                if self.inflation_dest is not None
                else None
            ),
            "flags": self.flags.to_json_dict(),
            "home_domain": self.home_domain.to_json_dict(),
            "thresholds": self.thresholds.to_json_dict(),
            "signers": [item.to_json_dict() for item in self.signers],
            "ext": self.ext.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> AccountEntry:
        account_id = AccountID.from_json_dict(json_dict["account_id"])
        balance = Int64.from_json_dict(json_dict["balance"])
        seq_num = SequenceNumber.from_json_dict(json_dict["seq_num"])
        num_sub_entries = Uint32.from_json_dict(json_dict["num_sub_entries"])
        inflation_dest = (
            AccountID.from_json_dict(json_dict["inflation_dest"])
            if json_dict["inflation_dest"] is not None
            else None
        )
        flags = Uint32.from_json_dict(json_dict["flags"])
        home_domain = String32.from_json_dict(json_dict["home_domain"])
        thresholds = Thresholds.from_json_dict(json_dict["thresholds"])
        signers = [Signer.from_json_dict(item) for item in json_dict["signers"]]
        ext = AccountEntryExt.from_json_dict(json_dict["ext"])
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

    def __hash__(self):
        return hash(
            (
                self.account_id,
                self.balance,
                self.seq_num,
                self.num_sub_entries,
                self.inflation_dest,
                self.flags,
                self.home_domain,
                self.thresholds,
                self.signers,
                self.ext,
            )
        )

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

    def __repr__(self):
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
        return f"<AccountEntry [{', '.join(out)}]>"
