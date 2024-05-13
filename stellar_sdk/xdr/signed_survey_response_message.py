# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .signature import Signature
from .survey_response_message import SurveyResponseMessage

__all__ = ["SignedSurveyResponseMessage"]


class SignedSurveyResponseMessage:
    """
    XDR Source Code::

        struct SignedSurveyResponseMessage
        {
            Signature responseSignature;
            SurveyResponseMessage response;
        };
    """

    def __init__(
        self,
        response_signature: Signature,
        response: SurveyResponseMessage,
    ) -> None:
        self.response_signature = response_signature
        self.response = response

    def pack(self, packer: Packer) -> None:
        self.response_signature.pack(packer)
        self.response.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SignedSurveyResponseMessage:
        response_signature = Signature.unpack(unpacker)
        response = SurveyResponseMessage.unpack(unpacker)
        return cls(
            response_signature=response_signature,
            response=response,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SignedSurveyResponseMessage:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SignedSurveyResponseMessage:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
        return f"<SignedSurveyResponseMessage [{', '.join(out)}]>"
