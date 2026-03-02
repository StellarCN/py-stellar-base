# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_TRUST_LINE_FLAGS_MAP = {
    1: "authorized_flag",
    2: "authorized_to_maintain_liabilities_flag",
    4: "trustline_clawback_enabled_flag",
}
_TRUST_LINE_FLAGS_REVERSE_MAP = {
    "authorized_flag": 1,
    "authorized_to_maintain_liabilities_flag": 2,
    "trustline_clawback_enabled_flag": 4,
}
__all__ = ["TrustLineFlags"]


class TrustLineFlags(IntEnum):
    """
    XDR Source Code::

        enum TrustLineFlags
        {
            // issuer has authorized account to perform transactions with its credit
            AUTHORIZED_FLAG = 1,
            // issuer has authorized account to maintain and reduce liabilities for its
            // credit
            AUTHORIZED_TO_MAINTAIN_LIABILITIES_FLAG = 2,
            // issuer has specified that it may clawback its credit, and that claimable
            // balances created with its credit may also be clawed back
            TRUSTLINE_CLAWBACK_ENABLED_FLAG = 4
        };
    """

    AUTHORIZED_FLAG = 1
    AUTHORIZED_TO_MAINTAIN_LIABILITIES_FLAG = 2
    TRUSTLINE_CLAWBACK_ENABLED_FLAG = 4

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> TrustLineFlags:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TrustLineFlags:
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
    def from_xdr(cls, xdr: str) -> TrustLineFlags:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TrustLineFlags:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _TRUST_LINE_FLAGS_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> TrustLineFlags:
        return cls(_TRUST_LINE_FLAGS_REVERSE_MAP[json_value])
