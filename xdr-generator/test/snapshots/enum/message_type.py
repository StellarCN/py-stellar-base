# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING
from xdrlib3 import Packer, Unpacker
from .base import DEFAULT_XDR_MAX_DEPTH, Integer, UnsignedInteger, Float, Double, Hyper, UnsignedHyper, Boolean, String, Opaque
from .constants import *

_MESSAGE_TYPE_MAP = {0: "error_msg", 1: "hello", 2: "dont_have", 3: "get_peers", 4: "peers", 5: "get_tx_set", 6: "tx_set", 7: "get_validations", 8: "validations", 9: "transaction", 10: "json_transaction", 11: "get_fba_quorumset", 12: "fba_quorumset", 13: "fba_message"}
_MESSAGE_TYPE_REVERSE_MAP = {"error_msg": 0, "hello": 1, "dont_have": 2, "get_peers": 3, "peers": 4, "get_tx_set": 5, "tx_set": 6, "get_validations": 7, "validations": 8, "transaction": 9, "json_transaction": 10, "get_fba_quorumset": 11, "fba_quorumset": 12, "fba_message": 13}
__all__ = ['MessageType']
class MessageType(IntEnum):
    """
    XDR Source Code::

        enum MessageType
        {
            ERROR_MSG,    
            HELLO,
            DONT_HAVE,

            GET_PEERS,   // gets a list of peers this guy knows about        
            PEERS,

            GET_TX_SET,  // gets a particular txset by hash        
            TX_SET,    

            GET_VALIDATIONS, // gets validations for a given ledger hash        
            VALIDATIONS,    

            TRANSACTION, //pass on a tx you have heard about        
            JSON_TRANSACTION,

            // FBA        
            GET_FBA_QUORUMSET,        
            FBA_QUORUMSET,    
            FBA_MESSAGE
        };
    """
    ERROR_MSG = 0
    HELLO = 1
    DONT_HAVE = 2
    GET_PEERS = 3
    PEERS = 4
    GET_TX_SET = 5
    TX_SET = 6
    GET_VALIDATIONS = 7
    VALIDATIONS = 8
    TRANSACTION = 9
    JSON_TRANSACTION = 10
    GET_FBA_QUORUMSET = 11
    FBA_QUORUMSET = 12
    FBA_MESSAGE = 13
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
