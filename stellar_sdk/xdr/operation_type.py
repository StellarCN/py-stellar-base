# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from enum import IntEnum
from xdrlib import Packer, Unpacker

from ..__version__ import __issues__
from ..exceptions import ValueError

__all__ = ["OperationType"]


class OperationType(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum OperationType
    {
        CREATE_ACCOUNT = 0,
        PAYMENT = 1,
        PATH_PAYMENT_STRICT_RECEIVE = 2,
        MANAGE_SELL_OFFER = 3,
        CREATE_PASSIVE_SELL_OFFER = 4,
        SET_OPTIONS = 5,
        CHANGE_TRUST = 6,
        ALLOW_TRUST = 7,
        ACCOUNT_MERGE = 8,
        INFLATION = 9,
        MANAGE_DATA = 10,
        BUMP_SEQUENCE = 11,
        MANAGE_BUY_OFFER = 12,
        PATH_PAYMENT_STRICT_SEND = 13,
        CREATE_CLAIMABLE_BALANCE = 14,
        CLAIM_CLAIMABLE_BALANCE = 15,
        BEGIN_SPONSORING_FUTURE_RESERVES = 16,
        END_SPONSORING_FUTURE_RESERVES = 17,
        REVOKE_SPONSORSHIP = 18,
        CLAWBACK = 19,
        CLAWBACK_CLAIMABLE_BALANCE = 20,
        SET_TRUST_LINE_FLAGS = 21
    };
    ----------------------------------------------------------------
    """

    CREATE_ACCOUNT = 0
    PAYMENT = 1
    PATH_PAYMENT_STRICT_RECEIVE = 2
    MANAGE_SELL_OFFER = 3
    CREATE_PASSIVE_SELL_OFFER = 4
    SET_OPTIONS = 5
    CHANGE_TRUST = 6
    ALLOW_TRUST = 7
    ACCOUNT_MERGE = 8
    INFLATION = 9
    MANAGE_DATA = 10
    BUMP_SEQUENCE = 11
    MANAGE_BUY_OFFER = 12
    PATH_PAYMENT_STRICT_SEND = 13
    CREATE_CLAIMABLE_BALANCE = 14
    CLAIM_CLAIMABLE_BALANCE = 15
    BEGIN_SPONSORING_FUTURE_RESERVES = 16
    END_SPONSORING_FUTURE_RESERVES = 17
    REVOKE_SPONSORSHIP = 18
    CLAWBACK = 19
    CLAWBACK_CLAIMABLE_BALANCE = 20
    SET_TRUST_LINE_FLAGS = 21

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "OperationType":
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "OperationType":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "OperationType":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )
