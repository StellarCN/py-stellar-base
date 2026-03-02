# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_ACCOUNT_MERGE_RESULT_CODE_MAP = {
    0: "success",
    -1: "malformed",
    -2: "no_account",
    -3: "immutable_set",
    -4: "has_sub_entries",
    -5: "seqnum_too_far",
    -6: "dest_full",
    -7: "is_sponsor",
}
_ACCOUNT_MERGE_RESULT_CODE_REVERSE_MAP = {
    "success": 0,
    "malformed": -1,
    "no_account": -2,
    "immutable_set": -3,
    "has_sub_entries": -4,
    "seqnum_too_far": -5,
    "dest_full": -6,
    "is_sponsor": -7,
}
__all__ = ["AccountMergeResultCode"]


class AccountMergeResultCode(IntEnum):
    """
    XDR Source Code::

        enum AccountMergeResultCode
        {
            // codes considered as "success" for the operation
            ACCOUNT_MERGE_SUCCESS = 0,
            // codes considered as "failure" for the operation
            ACCOUNT_MERGE_MALFORMED = -1,       // can't merge onto itself
            ACCOUNT_MERGE_NO_ACCOUNT = -2,      // destination does not exist
            ACCOUNT_MERGE_IMMUTABLE_SET = -3,   // source account has AUTH_IMMUTABLE set
            ACCOUNT_MERGE_HAS_SUB_ENTRIES = -4, // account has trust lines/offers
            ACCOUNT_MERGE_SEQNUM_TOO_FAR = -5,  // sequence number is over max allowed
            ACCOUNT_MERGE_DEST_FULL = -6,       // can't add source balance to
                                                // destination balance
            ACCOUNT_MERGE_IS_SPONSOR = -7       // can't merge account that is a sponsor
        };
    """

    ACCOUNT_MERGE_SUCCESS = 0
    ACCOUNT_MERGE_MALFORMED = -1
    ACCOUNT_MERGE_NO_ACCOUNT = -2
    ACCOUNT_MERGE_IMMUTABLE_SET = -3
    ACCOUNT_MERGE_HAS_SUB_ENTRIES = -4
    ACCOUNT_MERGE_SEQNUM_TOO_FAR = -5
    ACCOUNT_MERGE_DEST_FULL = -6
    ACCOUNT_MERGE_IS_SPONSOR = -7

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> AccountMergeResultCode:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> AccountMergeResultCode:
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
    def from_xdr(cls, xdr: str) -> AccountMergeResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> AccountMergeResultCode:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _ACCOUNT_MERGE_RESULT_CODE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> AccountMergeResultCode:
        return cls(_ACCOUNT_MERGE_RESULT_CODE_REVERSE_MAP[json_value])
