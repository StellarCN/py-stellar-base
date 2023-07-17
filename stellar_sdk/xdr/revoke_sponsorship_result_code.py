# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

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
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> RevokeSponsorshipResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
