# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_REVOKE_SPONSORSHIP_RESULT_CODE_MAP = {
    0: "success",
    -1: "does_not_exist",
    -2: "not_sponsor",
    -3: "low_reserve",
    -4: "only_transferable",
    -5: "malformed",
}
_REVOKE_SPONSORSHIP_RESULT_CODE_REVERSE_MAP = {
    "success": 0,
    "does_not_exist": -1,
    "not_sponsor": -2,
    "low_reserve": -3,
    "only_transferable": -4,
    "malformed": -5,
}
__all__ = ["RevokeSponsorshipResultCode"]


class RevokeSponsorshipResultCode(IntEnum):
    """
    XDR Source Code::

        enum RevokeSponsorshipResultCode
        {
            // codes considered as "success" for the operation
            REVOKE_SPONSORSHIP_SUCCESS = 0,

            // codes considered as "failure" for the operation
            REVOKE_SPONSORSHIP_DOES_NOT_EXIST = -1,
            REVOKE_SPONSORSHIP_NOT_SPONSOR = -2,
            REVOKE_SPONSORSHIP_LOW_RESERVE = -3,
            REVOKE_SPONSORSHIP_ONLY_TRANSFERABLE = -4,
            REVOKE_SPONSORSHIP_MALFORMED = -5
        };
    """

    REVOKE_SPONSORSHIP_SUCCESS = 0
    REVOKE_SPONSORSHIP_DOES_NOT_EXIST = -1
    REVOKE_SPONSORSHIP_NOT_SPONSOR = -2
    REVOKE_SPONSORSHIP_LOW_RESERVE = -3
    REVOKE_SPONSORSHIP_ONLY_TRANSFERABLE = -4
    REVOKE_SPONSORSHIP_MALFORMED = -5

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> RevokeSponsorshipResultCode:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> RevokeSponsorshipResultCode:
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
    def from_xdr(cls, xdr: str) -> RevokeSponsorshipResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> RevokeSponsorshipResultCode:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _REVOKE_SPONSORSHIP_RESULT_CODE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> RevokeSponsorshipResultCode:
        return cls(_REVOKE_SPONSORSHIP_RESULT_CODE_REVERSE_MAP[json_value])
