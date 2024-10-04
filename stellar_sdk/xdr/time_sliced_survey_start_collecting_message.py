# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .node_id import NodeID
from .uint32 import Uint32

__all__ = ["TimeSlicedSurveyStartCollectingMessage"]


class TimeSlicedSurveyStartCollectingMessage:
    """
    XDR Source Code::

        struct TimeSlicedSurveyStartCollectingMessage
        {
            NodeID surveyorID;
            uint32 nonce;
            uint32 ledgerNum;
        };
    """

    def __init__(
        self,
        surveyor_id: NodeID,
        nonce: Uint32,
        ledger_num: Uint32,
    ) -> None:
        self.surveyor_id = surveyor_id
        self.nonce = nonce
        self.ledger_num = ledger_num

    def pack(self, packer: Packer) -> None:
        self.surveyor_id.pack(packer)
        self.nonce.pack(packer)
        self.ledger_num.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> TimeSlicedSurveyStartCollectingMessage:
        surveyor_id = NodeID.unpack(unpacker)
        nonce = Uint32.unpack(unpacker)
        ledger_num = Uint32.unpack(unpacker)
        return cls(
            surveyor_id=surveyor_id,
            nonce=nonce,
            ledger_num=ledger_num,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TimeSlicedSurveyStartCollectingMessage:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> TimeSlicedSurveyStartCollectingMessage:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.surveyor_id,
                self.nonce,
                self.ledger_num,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.surveyor_id == other.surveyor_id
            and self.nonce == other.nonce
            and self.ledger_num == other.ledger_num
        )

    def __repr__(self):
        out = [
            f"surveyor_id={self.surveyor_id}",
            f"nonce={self.nonce}",
            f"ledger_num={self.ledger_num}",
        ]
        return f"<TimeSlicedSurveyStartCollectingMessage [{', '.join(out)}]>"
