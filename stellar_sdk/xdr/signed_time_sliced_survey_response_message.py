# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .signature import Signature
from .time_sliced_survey_response_message import TimeSlicedSurveyResponseMessage

__all__ = ["SignedTimeSlicedSurveyResponseMessage"]


class SignedTimeSlicedSurveyResponseMessage:
    """
    XDR Source Code::

        struct SignedTimeSlicedSurveyResponseMessage
        {
            Signature responseSignature;
            TimeSlicedSurveyResponseMessage response;
        };
    """

    def __init__(
        self,
        response_signature: Signature,
        response: TimeSlicedSurveyResponseMessage,
    ) -> None:
        self.response_signature = response_signature
        self.response = response

    def pack(self, packer: Packer) -> None:
        self.response_signature.pack(packer)
        self.response.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SignedTimeSlicedSurveyResponseMessage:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        response_signature = Signature.unpack(unpacker, depth_limit - 1)
        response = TimeSlicedSurveyResponseMessage.unpack(unpacker, depth_limit - 1)
        return cls(
            response_signature=response_signature,
            response=response,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SignedTimeSlicedSurveyResponseMessage:
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
    def from_xdr(cls, xdr: str) -> SignedTimeSlicedSurveyResponseMessage:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SignedTimeSlicedSurveyResponseMessage:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "response_signature": self.response_signature.to_json_dict(),
            "response": self.response.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SignedTimeSlicedSurveyResponseMessage:
        response_signature = Signature.from_json_dict(json_dict["response_signature"])
        response = TimeSlicedSurveyResponseMessage.from_json_dict(json_dict["response"])
        return cls(
            response_signature=response_signature,
            response=response,
        )

    def __hash__(self):
        return hash(
            (
                self.response_signature,
                self.response,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.response_signature == other.response_signature
            and self.response == other.response
        )

    def __repr__(self):
        out = [
            f"response_signature={self.response_signature}",
            f"response={self.response}",
        ]
        return f"<SignedTimeSlicedSurveyResponseMessage [{', '.join(out)}]>"
