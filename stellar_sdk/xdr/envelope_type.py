# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_ENVELOPE_TYPE_MAP = {
    0: "tx_v0",
    1: "scp",
    2: "tx",
    3: "auth",
    4: "scpvalue",
    5: "tx_fee_bump",
    6: "op_id",
    7: "pool_revoke_op_id",
    8: "contract_id",
    9: "soroban_authorization",
}
_ENVELOPE_TYPE_REVERSE_MAP = {
    "tx_v0": 0,
    "scp": 1,
    "tx": 2,
    "auth": 3,
    "scpvalue": 4,
    "tx_fee_bump": 5,
    "op_id": 6,
    "pool_revoke_op_id": 7,
    "contract_id": 8,
    "soroban_authorization": 9,
}
__all__ = ["EnvelopeType"]


class EnvelopeType(IntEnum):
    """
    XDR Source Code::

        enum EnvelopeType
        {
            ENVELOPE_TYPE_TX_V0 = 0,
            ENVELOPE_TYPE_SCP = 1,
            ENVELOPE_TYPE_TX = 2,
            ENVELOPE_TYPE_AUTH = 3,
            ENVELOPE_TYPE_SCPVALUE = 4,
            ENVELOPE_TYPE_TX_FEE_BUMP = 5,
            ENVELOPE_TYPE_OP_ID = 6,
            ENVELOPE_TYPE_POOL_REVOKE_OP_ID = 7,
            ENVELOPE_TYPE_CONTRACT_ID = 8,
            ENVELOPE_TYPE_SOROBAN_AUTHORIZATION = 9
        };
    """

    ENVELOPE_TYPE_TX_V0 = 0
    ENVELOPE_TYPE_SCP = 1
    ENVELOPE_TYPE_TX = 2
    ENVELOPE_TYPE_AUTH = 3
    ENVELOPE_TYPE_SCPVALUE = 4
    ENVELOPE_TYPE_TX_FEE_BUMP = 5
    ENVELOPE_TYPE_OP_ID = 6
    ENVELOPE_TYPE_POOL_REVOKE_OP_ID = 7
    ENVELOPE_TYPE_CONTRACT_ID = 8
    ENVELOPE_TYPE_SOROBAN_AUTHORIZATION = 9

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> EnvelopeType:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> EnvelopeType:
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
    def from_xdr(cls, xdr: str) -> EnvelopeType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> EnvelopeType:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _ENVELOPE_TYPE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> EnvelopeType:
        return cls(_ENVELOPE_TYPE_REVERSE_MAP[json_value])
