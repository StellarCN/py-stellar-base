# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

__all__ = ["SurveyMessageResponseType"]


class SurveyMessageResponseType(IntEnum):
    """
    XDR Source Code::

        enum SurveyMessageResponseType
        {
            SURVEY_TOPOLOGY_RESPONSE_V0 = 0,
            SURVEY_TOPOLOGY_RESPONSE_V1 = 1,
            SURVEY_TOPOLOGY_RESPONSE_V2 = 2
        };
    """

    SURVEY_TOPOLOGY_RESPONSE_V0 = 0
    SURVEY_TOPOLOGY_RESPONSE_V1 = 1
    SURVEY_TOPOLOGY_RESPONSE_V2 = 2

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SurveyMessageResponseType:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SurveyMessageResponseType:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SurveyMessageResponseType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
