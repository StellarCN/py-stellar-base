# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .signature import Signature
from .time_sliced_survey_request_message import TimeSlicedSurveyRequestMessage

__all__ = ["SignedTimeSlicedSurveyRequestMessage"]


class SignedTimeSlicedSurveyRequestMessage:
    """
    XDR Source Code::

        struct SignedTimeSlicedSurveyRequestMessage
        {
            Signature requestSignature;
            TimeSlicedSurveyRequestMessage request;
        };
    """

    def __init__(
        self,
        request_signature: Signature,
        request: TimeSlicedSurveyRequestMessage,
    ) -> None:
        self.request_signature = request_signature
        self.request = request

    def pack(self, packer: Packer) -> None:
        self.request_signature.pack(packer)
        self.request.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SignedTimeSlicedSurveyRequestMessage:
        request_signature = Signature.unpack(unpacker)
        request = TimeSlicedSurveyRequestMessage.unpack(unpacker)
        return cls(
            request_signature=request_signature,
            request=request,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SignedTimeSlicedSurveyRequestMessage:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SignedTimeSlicedSurveyRequestMessage:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.request_signature,
                self.request,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.request_signature == other.request_signature
            and self.request == other.request
        )

    def __repr__(self):
        out = [
            f"request_signature={self.request_signature}",
            f"request={self.request}",
        ]
        return f"<SignedTimeSlicedSurveyRequestMessage [{', '.join(out)}]>"
