# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_OPERATION_TYPE_MAP = {
    0: "create_account",
    1: "payment",
    2: "path_payment_strict_receive",
    3: "manage_sell_offer",
    4: "create_passive_sell_offer",
    5: "set_options",
    6: "change_trust",
    7: "allow_trust",
    8: "account_merge",
    9: "inflation",
    10: "manage_data",
    11: "bump_sequence",
    12: "manage_buy_offer",
    13: "path_payment_strict_send",
    14: "create_claimable_balance",
    15: "claim_claimable_balance",
    16: "begin_sponsoring_future_reserves",
    17: "end_sponsoring_future_reserves",
    18: "revoke_sponsorship",
    19: "clawback",
    20: "clawback_claimable_balance",
    21: "set_trust_line_flags",
    22: "liquidity_pool_deposit",
    23: "liquidity_pool_withdraw",
    24: "invoke_host_function",
    25: "extend_footprint_ttl",
    26: "restore_footprint",
}
_OPERATION_TYPE_REVERSE_MAP = {
    "create_account": 0,
    "payment": 1,
    "path_payment_strict_receive": 2,
    "manage_sell_offer": 3,
    "create_passive_sell_offer": 4,
    "set_options": 5,
    "change_trust": 6,
    "allow_trust": 7,
    "account_merge": 8,
    "inflation": 9,
    "manage_data": 10,
    "bump_sequence": 11,
    "manage_buy_offer": 12,
    "path_payment_strict_send": 13,
    "create_claimable_balance": 14,
    "claim_claimable_balance": 15,
    "begin_sponsoring_future_reserves": 16,
    "end_sponsoring_future_reserves": 17,
    "revoke_sponsorship": 18,
    "clawback": 19,
    "clawback_claimable_balance": 20,
    "set_trust_line_flags": 21,
    "liquidity_pool_deposit": 22,
    "liquidity_pool_withdraw": 23,
    "invoke_host_function": 24,
    "extend_footprint_ttl": 25,
    "restore_footprint": 26,
}
__all__ = ["OperationType"]


class OperationType(IntEnum):
    """
    XDR Source Code::

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
            SET_TRUST_LINE_FLAGS = 21,
            LIQUIDITY_POOL_DEPOSIT = 22,
            LIQUIDITY_POOL_WITHDRAW = 23,
            INVOKE_HOST_FUNCTION = 24,
            EXTEND_FOOTPRINT_TTL = 25,
            RESTORE_FOOTPRINT = 26
        };
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
    LIQUIDITY_POOL_DEPOSIT = 22
    LIQUIDITY_POOL_WITHDRAW = 23
    INVOKE_HOST_FUNCTION = 24
    EXTEND_FOOTPRINT_TTL = 25
    RESTORE_FOOTPRINT = 26

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> OperationType:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> OperationType:
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
    def from_xdr(cls, xdr: str) -> OperationType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> OperationType:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _OPERATION_TYPE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> OperationType:
        return cls(_OPERATION_TYPE_REVERSE_MAP[json_value])
