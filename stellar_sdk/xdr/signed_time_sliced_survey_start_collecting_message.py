# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .signature import Signature
from .time_sliced_survey_start_collecting_message import (
    TimeSlicedSurveyStartCollectingMessage,
)

__all__ = ["SignedTimeSlicedSurveyStartCollectingMessage"]


class SignedTimeSlicedSurveyStartCollectingMessage:
    """
    XDR Source Code::

        struct SignedTimeSlicedSurveyStartCollectingMessage
        {
            Signature signature;
            TimeSlicedSurveyStartCollectingMessage startCollecting;
        };
    """

    def __init__(
        self,
        signature: Signature,
        start_collecting: TimeSlicedSurveyStartCollectingMessage,
    ) -> None:
        self.signature = signature
        self.start_collecting = start_collecting

    def pack(self, packer: Packer) -> None:
        self.signature.pack(packer)
        self.start_collecting.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SignedTimeSlicedSurveyStartCollectingMessage:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        signature = Signature.unpack(unpacker, depth_limit - 1)
        start_collecting = TimeSlicedSurveyStartCollectingMessage.unpack(
            unpacker, depth_limit - 1
        )
        return cls(
            signature=signature,
            start_collecting=start_collecting,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SignedTimeSlicedSurveyStartCollectingMessage:
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
    def from_xdr(cls, xdr: str) -> SignedTimeSlicedSurveyStartCollectingMessage:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SignedTimeSlicedSurveyStartCollectingMessage:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "signature": self.signature.to_json_dict(),
            "start_collecting": self.start_collecting.to_json_dict(),
        }

    @classmethod
    def from_json_dict(
        cls, json_dict: dict
    ) -> SignedTimeSlicedSurveyStartCollectingMessage:
        signature = Signature.from_json_dict(json_dict["signature"])
        start_collecting = TimeSlicedSurveyStartCollectingMessage.from_json_dict(
            json_dict["start_collecting"]
        )
        return cls(
            signature=signature,
            start_collecting=start_collecting,
        )

    def __hash__(self):
        return hash(
            (
                self.signature,
                self.start_collecting,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.signature == other.signature
            and self.start_collecting == other.start_collecting
        )

    def __repr__(self):
        out = [
            f"signature={self.signature}",
            f"start_collecting={self.start_collecting}",
        ]
        return f"<SignedTimeSlicedSurveyStartCollectingMessage [{', '.join(out)}]>"
