# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

__all__ = ["TransactionResultCode"]


class TransactionResultCode(IntEnum):
    """
    XDR Source Code::

        enum TransactionResultCode
        {
            txFEE_BUMP_INNER_SUCCESS = 1, // fee bump inner transaction succeeded
            txSUCCESS = 0,                // all operations succeeded

            txFAILED = -1, // one of the operations failed (none were applied)

            txTOO_EARLY = -2,         // ledger closeTime before minTime
            txTOO_LATE = -3,          // ledger closeTime after maxTime
            txMISSING_OPERATION = -4, // no operation was specified
            txBAD_SEQ = -5,           // sequence number does not match source account

            txBAD_AUTH = -6,             // too few valid signatures / wrong network
            txINSUFFICIENT_BALANCE = -7, // fee would bring account below reserve
            txNO_ACCOUNT = -8,           // source account not found
            txINSUFFICIENT_FEE = -9,     // fee is too small
            txBAD_AUTH_EXTRA = -10,      // unused signatures attached to transaction
            txINTERNAL_ERROR = -11,      // an unknown error occurred

            txNOT_SUPPORTED = -12,          // transaction type not supported
            txFEE_BUMP_INNER_FAILED = -13,  // fee bump inner transaction failed
            txBAD_SPONSORSHIP = -14,        // sponsorship not confirmed
            txBAD_MIN_SEQ_AGE_OR_GAP = -15, // minSeqAge or minSeqLedgerGap conditions not met
            txMALFORMED = -16,              // precondition is invalid
            txSOROBAN_INVALID = -17         // soroban-specific preconditions were not met
        };
    """

    txFEE_BUMP_INNER_SUCCESS = 1
    txSUCCESS = 0
    txFAILED = -1
    txTOO_EARLY = -2
    txTOO_LATE = -3
    txMISSING_OPERATION = -4
    txBAD_SEQ = -5
    txBAD_AUTH = -6
    txINSUFFICIENT_BALANCE = -7
    txNO_ACCOUNT = -8
    txINSUFFICIENT_FEE = -9
    txBAD_AUTH_EXTRA = -10
    txINTERNAL_ERROR = -11
    txNOT_SUPPORTED = -12
    txFEE_BUMP_INNER_FAILED = -13
    txBAD_SPONSORSHIP = -14
    txBAD_MIN_SEQ_AGE_OR_GAP = -15
    txMALFORMED = -16
    txSOROBAN_INVALID = -17

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> TransactionResultCode:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TransactionResultCode:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> TransactionResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
