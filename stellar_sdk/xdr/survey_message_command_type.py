# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_SURVEY_MESSAGE_COMMAND_TYPE_MAP = {1: "time_sliced_survey_topology"}
_SURVEY_MESSAGE_COMMAND_TYPE_REVERSE_MAP = {"time_sliced_survey_topology": 1}
__all__ = ["SurveyMessageCommandType"]


class SurveyMessageCommandType(IntEnum):
    """
    XDR Source Code::

        enum SurveyMessageCommandType
        {
            TIME_SLICED_SURVEY_TOPOLOGY = 1
        };
    """

    TIME_SLICED_SURVEY_TOPOLOGY = 1

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SurveyMessageCommandType:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SurveyMessageCommandType:
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
    def from_xdr(cls, xdr: str) -> SurveyMessageCommandType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SurveyMessageCommandType:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _SURVEY_MESSAGE_COMMAND_TYPE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> SurveyMessageCommandType:
        return cls(_SURVEY_MESSAGE_COMMAND_TYPE_REVERSE_MAP[json_value])
