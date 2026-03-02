# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .node_id import NodeID
from .uint32 import Uint32

__all__ = ["TimeSlicedSurveyStopCollectingMessage"]


class TimeSlicedSurveyStopCollectingMessage:
    """
    XDR Source Code::

        struct TimeSlicedSurveyStopCollectingMessage
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> TimeSlicedSurveyStopCollectingMessage:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        surveyor_id = NodeID.unpack(unpacker, depth_limit - 1)
        nonce = Uint32.unpack(unpacker, depth_limit - 1)
        ledger_num = Uint32.unpack(unpacker, depth_limit - 1)
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
    def from_xdr_bytes(cls, xdr: bytes) -> TimeSlicedSurveyStopCollectingMessage:
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
    def from_xdr(cls, xdr: str) -> TimeSlicedSurveyStopCollectingMessage:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TimeSlicedSurveyStopCollectingMessage:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "surveyor_id": self.surveyor_id.to_json_dict(),
            "nonce": self.nonce.to_json_dict(),
            "ledger_num": self.ledger_num.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> TimeSlicedSurveyStopCollectingMessage:
        surveyor_id = NodeID.from_json_dict(json_dict["surveyor_id"])
        nonce = Uint32.from_json_dict(json_dict["nonce"])
        ledger_num = Uint32.from_json_dict(json_dict["ledger_num"])
        return cls(
            surveyor_id=surveyor_id,
            nonce=nonce,
            ledger_num=ledger_num,
        )

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
        return f"<TimeSlicedSurveyStopCollectingMessage [{', '.join(out)}]>"
