# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING
from xdrlib3 import Packer, Unpacker
from .base import Integer, UnsignedInteger, Float, Double, Hyper, UnsignedHyper, Boolean, String, Opaque
from .constants import *

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
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> MessageType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
