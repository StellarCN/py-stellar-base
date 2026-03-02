# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .account_merge_result_code import AccountMergeResultCode
from .base import DEFAULT_XDR_MAX_DEPTH
from .int64 import Int64

__all__ = ["AccountMergeResult"]


class AccountMergeResult:
    """
    XDR Source Code::

        union AccountMergeResult switch (AccountMergeResultCode code)
        {
        case ACCOUNT_MERGE_SUCCESS:
            int64 sourceAccountBalance; // how much got transferred from source account
        case ACCOUNT_MERGE_MALFORMED:
        case ACCOUNT_MERGE_NO_ACCOUNT:
        case ACCOUNT_MERGE_IMMUTABLE_SET:
        case ACCOUNT_MERGE_HAS_SUB_ENTRIES:
        case ACCOUNT_MERGE_SEQNUM_TOO_FAR:
        case ACCOUNT_MERGE_DEST_FULL:
        case ACCOUNT_MERGE_IS_SPONSOR:
            void;
        };
    """

    def __init__(
        self,
        code: AccountMergeResultCode,
        source_account_balance: Optional[Int64] = None,
    ) -> None:
        self.code = code
        self.source_account_balance = source_account_balance

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == AccountMergeResultCode.ACCOUNT_MERGE_SUCCESS:
            if self.source_account_balance is None:
                raise ValueError("source_account_balance should not be None.")
            self.source_account_balance.pack(packer)
            return
        if self.code == AccountMergeResultCode.ACCOUNT_MERGE_MALFORMED:
            return
        if self.code == AccountMergeResultCode.ACCOUNT_MERGE_NO_ACCOUNT:
            return
        if self.code == AccountMergeResultCode.ACCOUNT_MERGE_IMMUTABLE_SET:
            return
        if self.code == AccountMergeResultCode.ACCOUNT_MERGE_HAS_SUB_ENTRIES:
            return
        if self.code == AccountMergeResultCode.ACCOUNT_MERGE_SEQNUM_TOO_FAR:
            return
        if self.code == AccountMergeResultCode.ACCOUNT_MERGE_DEST_FULL:
            return
        if self.code == AccountMergeResultCode.ACCOUNT_MERGE_IS_SPONSOR:
            return
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> AccountMergeResult:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        code = AccountMergeResultCode.unpack(unpacker)
        if code == AccountMergeResultCode.ACCOUNT_MERGE_SUCCESS:
            source_account_balance = Int64.unpack(unpacker, depth_limit - 1)
            return cls(code=code, source_account_balance=source_account_balance)
        if code == AccountMergeResultCode.ACCOUNT_MERGE_MALFORMED:
            return cls(code=code)
        if code == AccountMergeResultCode.ACCOUNT_MERGE_NO_ACCOUNT:
            return cls(code=code)
        if code == AccountMergeResultCode.ACCOUNT_MERGE_IMMUTABLE_SET:
            return cls(code=code)
        if code == AccountMergeResultCode.ACCOUNT_MERGE_HAS_SUB_ENTRIES:
            return cls(code=code)
        if code == AccountMergeResultCode.ACCOUNT_MERGE_SEQNUM_TOO_FAR:
            return cls(code=code)
        if code == AccountMergeResultCode.ACCOUNT_MERGE_DEST_FULL:
            return cls(code=code)
        if code == AccountMergeResultCode.ACCOUNT_MERGE_IS_SPONSOR:
            return cls(code=code)
        raise ValueError("Invalid code.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> AccountMergeResult:
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
    def from_xdr(cls, xdr: str) -> AccountMergeResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> AccountMergeResult:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.code == AccountMergeResultCode.ACCOUNT_MERGE_SUCCESS:
            assert self.source_account_balance is not None
            return {"success": self.source_account_balance.to_json_dict()}
        if self.code == AccountMergeResultCode.ACCOUNT_MERGE_MALFORMED:
            return "malformed"
        if self.code == AccountMergeResultCode.ACCOUNT_MERGE_NO_ACCOUNT:
            return "no_account"
        if self.code == AccountMergeResultCode.ACCOUNT_MERGE_IMMUTABLE_SET:
            return "immutable_set"
        if self.code == AccountMergeResultCode.ACCOUNT_MERGE_HAS_SUB_ENTRIES:
            return "has_sub_entries"
        if self.code == AccountMergeResultCode.ACCOUNT_MERGE_SEQNUM_TOO_FAR:
            return "seqnum_too_far"
        if self.code == AccountMergeResultCode.ACCOUNT_MERGE_DEST_FULL:
            return "dest_full"
        if self.code == AccountMergeResultCode.ACCOUNT_MERGE_IS_SPONSOR:
            return "is_sponsor"
        raise ValueError(f"Unknown code in AccountMergeResult: {self.code}")

    @classmethod
    def from_json_dict(cls, json_value: str | dict) -> AccountMergeResult:
        if isinstance(json_value, str):
            if json_value not in (
                "malformed",
                "no_account",
                "immutable_set",
                "has_sub_entries",
                "seqnum_too_far",
                "dest_full",
                "is_sponsor",
            ):
                raise ValueError(
                    f"Unexpected string '{json_value}' for AccountMergeResult, must be one of: malformed, no_account, immutable_set, has_sub_entries, seqnum_too_far, dest_full, is_sponsor"
                )
            code = AccountMergeResultCode.from_json_dict(json_value)
            return cls(code=code)
        if not isinstance(json_value, dict) or len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for AccountMergeResult, got: {json_value}"
            )
        key = next(iter(json_value))
        code = AccountMergeResultCode.from_json_dict(key)
        if key == "success":
            source_account_balance = Int64.from_json_dict(json_value["success"])
            return cls(code=code, source_account_balance=source_account_balance)
        raise ValueError(f"Unknown key '{key}' for AccountMergeResult")

    def __hash__(self):
        return hash(
            (
                self.code,
                self.source_account_balance,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.code == other.code
            and self.source_account_balance == other.source_account_balance
        )

    def __repr__(self):
        out = []
        out.append(f"code={self.code}")
        if self.source_account_balance is not None:
            out.append(f"source_account_balance={self.source_account_balance}")
        return f"<AccountMergeResult [{', '.join(out)}]>"
