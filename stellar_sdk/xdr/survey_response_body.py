# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .survey_message_response_type import SurveyMessageResponseType
from .topology_response_body_v2 import TopologyResponseBodyV2

__all__ = ["SurveyResponseBody"]


class SurveyResponseBody:
    """
    XDR Source Code::

        union SurveyResponseBody switch (SurveyMessageResponseType type)
        {
        case SURVEY_TOPOLOGY_RESPONSE_V2:
            TopologyResponseBodyV2 topologyResponseBodyV2;
        };
    """

    def __init__(
        self,
        type: SurveyMessageResponseType,
        topology_response_body_v2: Optional[TopologyResponseBodyV2] = None,
    ) -> None:
        self.type = type
        self.topology_response_body_v2 = topology_response_body_v2

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == SurveyMessageResponseType.SURVEY_TOPOLOGY_RESPONSE_V2:
            if self.topology_response_body_v2 is None:
                raise ValueError("topology_response_body_v2 should not be None.")
            self.topology_response_body_v2.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SurveyResponseBody:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = SurveyMessageResponseType.unpack(unpacker)
        if type == SurveyMessageResponseType.SURVEY_TOPOLOGY_RESPONSE_V2:
            topology_response_body_v2 = TopologyResponseBodyV2.unpack(
                unpacker, depth_limit - 1
            )
            return cls(type=type, topology_response_body_v2=topology_response_body_v2)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SurveyResponseBody:
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
    def from_xdr(cls, xdr: str) -> SurveyResponseBody:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SurveyResponseBody:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.type == SurveyMessageResponseType.SURVEY_TOPOLOGY_RESPONSE_V2:
            assert self.topology_response_body_v2 is not None
            return {
                "survey_topology_response_v2": self.topology_response_body_v2.to_json_dict()
            }
        raise ValueError(f"Unknown type in SurveyResponseBody: {self.type}")

    @classmethod
    def from_json_dict(cls, json_value: dict) -> SurveyResponseBody:
        if len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for SurveyResponseBody, got: {json_value}"
            )
        key = next(iter(json_value))
        type = SurveyMessageResponseType.from_json_dict(key)
        if key == "survey_topology_response_v2":
            topology_response_body_v2 = TopologyResponseBodyV2.from_json_dict(
                json_value["survey_topology_response_v2"]
            )
            return cls(type=type, topology_response_body_v2=topology_response_body_v2)
        raise ValueError(f"Unknown key '{key}' for SurveyResponseBody")

    def __hash__(self):
        return hash(
            (
                self.type,
                self.topology_response_body_v2,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.topology_response_body_v2 == other.topology_response_body_v2
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        if self.topology_response_body_v2 is not None:
            out.append(f"topology_response_body_v2={self.topology_response_body_v2}")
        return f"<SurveyResponseBody [{', '.join(out)}]>"
