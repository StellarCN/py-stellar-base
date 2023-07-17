# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

__all__ = ["CreateAccountResultCode"]


class CreateAccountResultCode(IntEnum):
    """
    XDR Source Code::

        enum CreateAccountResultCode
        {
            // codes considered as "success" for the operation
            CREATE_ACCOUNT_SUCCESS = 0, // account was created

            // codes considered as "failure" for the operation
            CREATE_ACCOUNT_MALFORMED = -1,   // invalid destination
            CREATE_ACCOUNT_UNDERFUNDED = -2, // not enough funds in source account
            CREATE_ACCOUNT_LOW_RESERVE =
                -3, // would create an account below the min reserve
            CREATE_ACCOUNT_ALREADY_EXIST = -4 // account already exists
        };
    """

    CREATE_ACCOUNT_SUCCESS = 0
    CREATE_ACCOUNT_MALFORMED = -1
    CREATE_ACCOUNT_UNDERFUNDED = -2
    CREATE_ACCOUNT_LOW_RESERVE = -3
    CREATE_ACCOUNT_ALREADY_EXIST = -4

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> CreateAccountResultCode:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> CreateAccountResultCode:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> CreateAccountResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
