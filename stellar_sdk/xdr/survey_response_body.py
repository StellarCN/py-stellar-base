# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import Optional

from xdrlib3 import Packer, Unpacker

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

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SurveyResponseBody:
        type = SurveyMessageResponseType.unpack(unpacker)
        if type == SurveyMessageResponseType.SURVEY_TOPOLOGY_RESPONSE_V2:
            topology_response_body_v2 = TopologyResponseBodyV2.unpack(unpacker)
            return cls(type=type, topology_response_body_v2=topology_response_body_v2)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SurveyResponseBody:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SurveyResponseBody:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
        (
            out.append(f"topology_response_body_v2={self.topology_response_body_v2}")
            if self.topology_response_body_v2 is not None
            else None
        )
        return f"<SurveyResponseBody [{', '.join(out)}]>"
