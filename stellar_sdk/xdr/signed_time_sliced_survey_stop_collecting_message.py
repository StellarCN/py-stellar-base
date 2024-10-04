# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .signature import Signature
from .time_sliced_survey_stop_collecting_message import (
    TimeSlicedSurveyStopCollectingMessage,
)

__all__ = ["SignedTimeSlicedSurveyStopCollectingMessage"]


class SignedTimeSlicedSurveyStopCollectingMessage:
    """
    XDR Source Code::

        struct SignedTimeSlicedSurveyStopCollectingMessage
        {
            Signature signature;
            TimeSlicedSurveyStopCollectingMessage stopCollecting;
        };
    """

    def __init__(
        self,
        signature: Signature,
        stop_collecting: TimeSlicedSurveyStopCollectingMessage,
    ) -> None:
        self.signature = signature
        self.stop_collecting = stop_collecting

    def pack(self, packer: Packer) -> None:
        self.signature.pack(packer)
        self.stop_collecting.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SignedTimeSlicedSurveyStopCollectingMessage:
        signature = Signature.unpack(unpacker)
        stop_collecting = TimeSlicedSurveyStopCollectingMessage.unpack(unpacker)
        return cls(
            signature=signature,
            stop_collecting=stop_collecting,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SignedTimeSlicedSurveyStopCollectingMessage:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SignedTimeSlicedSurveyStopCollectingMessage:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.signature,
                self.stop_collecting,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.signature == other.signature
            and self.stop_collecting == other.stop_collecting
        )

    def __repr__(self):
        out = [
            f"signature={self.signature}",
            f"stop_collecting={self.stop_collecting}",
        ]
        return f"<SignedTimeSlicedSurveyStopCollectingMessage [{', '.join(out)}]>"
