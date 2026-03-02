# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SignedTimeSlicedSurveyRequestMessage:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        request_signature = Signature.unpack(unpacker, depth_limit - 1)
        request = TimeSlicedSurveyRequestMessage.unpack(unpacker, depth_limit - 1)
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SignedTimeSlicedSurveyRequestMessage:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SignedTimeSlicedSurveyRequestMessage:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "request_signature": self.request_signature.to_json_dict(),
            "request": self.request.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SignedTimeSlicedSurveyRequestMessage:
        request_signature = Signature.from_json_dict(json_dict["request_signature"])
        request = TimeSlicedSurveyRequestMessage.from_json_dict(json_dict["request"])
        return cls(
            request_signature=request_signature,
            request=request,
        )

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
