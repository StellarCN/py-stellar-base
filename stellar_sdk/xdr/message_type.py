# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_MESSAGE_TYPE_MAP = {
    0: "error_msg",
    2: "auth",
    3: "dont_have",
    5: "peers",
    6: "get_tx_set",
    7: "tx_set",
    17: "generalized_tx_set",
    8: "transaction",
    9: "get_scp_quorumset",
    10: "scp_quorumset",
    11: "scp_message",
    12: "get_scp_state",
    13: "hello",
    16: "send_more",
    20: "send_more_extended",
    18: "flood_advert",
    19: "flood_demand",
    21: "time_sliced_survey_request",
    22: "time_sliced_survey_response",
    23: "time_sliced_survey_start_collecting",
    24: "time_sliced_survey_stop_collecting",
}
_MESSAGE_TYPE_REVERSE_MAP = {
    "error_msg": 0,
    "auth": 2,
    "dont_have": 3,
    "peers": 5,
    "get_tx_set": 6,
    "tx_set": 7,
    "generalized_tx_set": 17,
    "transaction": 8,
    "get_scp_quorumset": 9,
    "scp_quorumset": 10,
    "scp_message": 11,
    "get_scp_state": 12,
    "hello": 13,
    "send_more": 16,
    "send_more_extended": 20,
    "flood_advert": 18,
    "flood_demand": 19,
    "time_sliced_survey_request": 21,
    "time_sliced_survey_response": 22,
    "time_sliced_survey_start_collecting": 23,
    "time_sliced_survey_stop_collecting": 24,
}
__all__ = ["MessageType"]


class MessageType(IntEnum):
    """
    XDR Source Code::

        enum MessageType
        {
            ERROR_MSG = 0,
            AUTH = 2,
            DONT_HAVE = 3,
            // GET_PEERS (4) is deprecated

            PEERS = 5,

            GET_TX_SET = 6, // gets a particular txset by hash
            TX_SET = 7,
            GENERALIZED_TX_SET = 17,

            TRANSACTION = 8, // pass on a tx you have heard about

            // SCP
            GET_SCP_QUORUMSET = 9,
            SCP_QUORUMSET = 10,
            SCP_MESSAGE = 11,
            GET_SCP_STATE = 12,

            // new messages
            HELLO = 13,

            // SURVEY_REQUEST (14) removed and replaced by TIME_SLICED_SURVEY_REQUEST
            // SURVEY_RESPONSE (15) removed and replaced by TIME_SLICED_SURVEY_RESPONSE

            SEND_MORE = 16,
            SEND_MORE_EXTENDED = 20,

            FLOOD_ADVERT = 18,
            FLOOD_DEMAND = 19,

            TIME_SLICED_SURVEY_REQUEST = 21,
            TIME_SLICED_SURVEY_RESPONSE = 22,
            TIME_SLICED_SURVEY_START_COLLECTING = 23,
            TIME_SLICED_SURVEY_STOP_COLLECTING = 24
        };
    """

    ERROR_MSG = 0
    AUTH = 2
    DONT_HAVE = 3
    PEERS = 5
    GET_TX_SET = 6
    TX_SET = 7
    GENERALIZED_TX_SET = 17
    TRANSACTION = 8
    GET_SCP_QUORUMSET = 9
    SCP_QUORUMSET = 10
    SCP_MESSAGE = 11
    GET_SCP_STATE = 12
    HELLO = 13
    SEND_MORE = 16
    SEND_MORE_EXTENDED = 20
    FLOOD_ADVERT = 18
    FLOOD_DEMAND = 19
    TIME_SLICED_SURVEY_REQUEST = 21
    TIME_SLICED_SURVEY_RESPONSE = 22
    TIME_SLICED_SURVEY_START_COLLECTING = 23
    TIME_SLICED_SURVEY_STOP_COLLECTING = 24

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> MessageType:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> MessageType:
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
    def from_xdr(cls, xdr: str) -> MessageType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> MessageType:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _MESSAGE_TYPE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> MessageType:
        return cls(_MESSAGE_TYPE_REVERSE_MAP[json_value])
