# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_TRANSACTION_RESULT_CODE_MAP = {
    1: "txfee_bump_inner_success",
    0: "txsuccess",
    -1: "txfailed",
    -2: "txtoo_early",
    -3: "txtoo_late",
    -4: "txmissing_operation",
    -5: "txbad_seq",
    -6: "txbad_auth",
    -7: "txinsufficient_balance",
    -8: "txno_account",
    -9: "txinsufficient_fee",
    -10: "txbad_auth_extra",
    -11: "txinternal_error",
    -12: "txnot_supported",
    -13: "txfee_bump_inner_failed",
    -14: "txbad_sponsorship",
    -15: "txbad_min_seq_age_or_gap",
    -16: "txmalformed",
    -17: "txsoroban_invalid",
    -18: "txfrozen_key_accessed",
}
_TRANSACTION_RESULT_CODE_REVERSE_MAP = {
    "txfee_bump_inner_success": 1,
    "txsuccess": 0,
    "txfailed": -1,
    "txtoo_early": -2,
    "txtoo_late": -3,
    "txmissing_operation": -4,
    "txbad_seq": -5,
    "txbad_auth": -6,
    "txinsufficient_balance": -7,
    "txno_account": -8,
    "txinsufficient_fee": -9,
    "txbad_auth_extra": -10,
    "txinternal_error": -11,
    "txnot_supported": -12,
    "txfee_bump_inner_failed": -13,
    "txbad_sponsorship": -14,
    "txbad_min_seq_age_or_gap": -15,
    "txmalformed": -16,
    "txsoroban_invalid": -17,
    "txfrozen_key_accessed": -18,
}
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
            txSOROBAN_INVALID = -17,        // soroban-specific preconditions were not met
            txFROZEN_KEY_ACCESSED = -18     // a 'frozen' ledger key is accessed by any operation
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
    txFROZEN_KEY_ACCESSED = -18

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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> TransactionResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TransactionResultCode:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _TRANSACTION_RESULT_CODE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> TransactionResultCode:
        return cls(_TRANSACTION_RESULT_CODE_REVERSE_MAP[json_value])
