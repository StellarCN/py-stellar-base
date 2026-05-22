# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_ACCOUNT_FLAGS_MAP = {
    1: "required_flag",
    2: "revocable_flag",
    4: "immutable_flag",
    8: "clawback_enabled_flag",
}
_ACCOUNT_FLAGS_REVERSE_MAP = {
    "required_flag": 1,
    "revocable_flag": 2,
    "immutable_flag": 4,
    "clawback_enabled_flag": 8,
}
__all__ = ["AccountFlags"]


class AccountFlags(IntEnum):
    """
    XDR Source Code::

        enum AccountFlags
        { // masks for each flag

            // Flags set on issuer accounts
            // TrustLines are created with authorized set to "false" requiring
            // the issuer to set it for each TrustLine
            AUTH_REQUIRED_FLAG = 0x1,
            // If set, the authorized flag in TrustLines can be cleared
            // otherwise, authorization cannot be revoked
            AUTH_REVOCABLE_FLAG = 0x2,
            // Once set, causes all AUTH_* flags to be read-only
            AUTH_IMMUTABLE_FLAG = 0x4,
            // Trustlines are created with clawback enabled set to "true",
            // and claimable balances created from those trustlines are created
            // with clawback enabled set to "true"
            AUTH_CLAWBACK_ENABLED_FLAG = 0x8
        };
    """

    AUTH_REQUIRED_FLAG = 1
    AUTH_REVOCABLE_FLAG = 2
    AUTH_IMMUTABLE_FLAG = 4
    AUTH_CLAWBACK_ENABLED_FLAG = 8

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> AccountFlags:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> AccountFlags:
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
    def from_xdr(cls, xdr: str) -> AccountFlags:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> AccountFlags:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _ACCOUNT_FLAGS_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> AccountFlags:
        return cls(_ACCOUNT_FLAGS_REVERSE_MAP[json_value])
