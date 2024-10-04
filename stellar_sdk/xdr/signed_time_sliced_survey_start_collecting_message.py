# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

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
    def unpack(cls, unpacker: Unpacker) -> SignedTimeSlicedSurveyStartCollectingMessage:
        signature = Signature.unpack(unpacker)
        start_collecting = TimeSlicedSurveyStartCollectingMessage.unpack(unpacker)
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
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SignedTimeSlicedSurveyStartCollectingMessage:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
