# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .survey_response_message import SurveyResponseMessage
from .uint32 import Uint32

__all__ = ["TimeSlicedSurveyResponseMessage"]


class TimeSlicedSurveyResponseMessage:
    """
    XDR Source Code::

        struct TimeSlicedSurveyResponseMessage
        {
            SurveyResponseMessage response;
            uint32 nonce;
        };
    """

    def __init__(
        self,
        response: SurveyResponseMessage,
        nonce: Uint32,
    ) -> None:
        self.response = response
        self.nonce = nonce

    def pack(self, packer: Packer) -> None:
        self.response.pack(packer)
        self.nonce.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> TimeSlicedSurveyResponseMessage:
        response = SurveyResponseMessage.unpack(unpacker)
        nonce = Uint32.unpack(unpacker)
        return cls(
            response=response,
            nonce=nonce,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TimeSlicedSurveyResponseMessage:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> TimeSlicedSurveyResponseMessage:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.response,
                self.nonce,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.response == other.response and self.nonce == other.nonce

    def __repr__(self):
        out = [
            f"response={self.response}",
            f"nonce={self.nonce}",
        ]
        return f"<TimeSlicedSurveyResponseMessage [{', '.join(out)}]>"
