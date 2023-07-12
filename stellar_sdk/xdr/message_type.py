# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

__all__ = ["MessageType"]


class MessageType(IntEnum):
    """
    XDR Source Code::

        enum MessageType
        {
            ERROR_MSG = 0,
            AUTH = 2,
            DONT_HAVE = 3,

            GET_PEERS = 4, // gets a list of peers this guy knows about
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

            SURVEY_REQUEST = 14,
            SURVEY_RESPONSE = 15,

            SEND_MORE = 16,
            SEND_MORE_EXTENDED = 20,

            FLOOD_ADVERT = 18,
            FLOOD_DEMAND = 19
        };
    """

    ERROR_MSG = 0
    AUTH = 2
    DONT_HAVE = 3
    GET_PEERS = 4
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
    SURVEY_REQUEST = 14
    SURVEY_RESPONSE = 15
    SEND_MORE = 16
    SEND_MORE_EXTENDED = 20
    FLOOD_ADVERT = 18
    FLOOD_DEMAND = 19

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
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> MessageType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
