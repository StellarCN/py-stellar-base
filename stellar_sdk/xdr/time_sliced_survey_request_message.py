# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .survey_request_message import SurveyRequestMessage
from .uint32 import Uint32

__all__ = ["TimeSlicedSurveyRequestMessage"]


class TimeSlicedSurveyRequestMessage:
    """
    XDR Source Code::

        struct TimeSlicedSurveyRequestMessage
        {
            SurveyRequestMessage request;
            uint32 nonce;
            uint32 inboundPeersIndex;
            uint32 outboundPeersIndex;
        };
    """

    def __init__(
        self,
        request: SurveyRequestMessage,
        nonce: Uint32,
        inbound_peers_index: Uint32,
        outbound_peers_index: Uint32,
    ) -> None:
        self.request = request
        self.nonce = nonce
        self.inbound_peers_index = inbound_peers_index
        self.outbound_peers_index = outbound_peers_index

    def pack(self, packer: Packer) -> None:
        self.request.pack(packer)
        self.nonce.pack(packer)
        self.inbound_peers_index.pack(packer)
        self.outbound_peers_index.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> TimeSlicedSurveyRequestMessage:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        request = SurveyRequestMessage.unpack(unpacker, depth_limit - 1)
        nonce = Uint32.unpack(unpacker, depth_limit - 1)
        inbound_peers_index = Uint32.unpack(unpacker, depth_limit - 1)
        outbound_peers_index = Uint32.unpack(unpacker, depth_limit - 1)
        return cls(
            request=request,
            nonce=nonce,
            inbound_peers_index=inbound_peers_index,
            outbound_peers_index=outbound_peers_index,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TimeSlicedSurveyRequestMessage:
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
    def from_xdr(cls, xdr: str) -> TimeSlicedSurveyRequestMessage:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TimeSlicedSurveyRequestMessage:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "request": self.request.to_json_dict(),
            "nonce": self.nonce.to_json_dict(),
            "inbound_peers_index": self.inbound_peers_index.to_json_dict(),
            "outbound_peers_index": self.outbound_peers_index.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> TimeSlicedSurveyRequestMessage:
        request = SurveyRequestMessage.from_json_dict(json_dict["request"])
        nonce = Uint32.from_json_dict(json_dict["nonce"])
        inbound_peers_index = Uint32.from_json_dict(json_dict["inbound_peers_index"])
        outbound_peers_index = Uint32.from_json_dict(json_dict["outbound_peers_index"])
        return cls(
            request=request,
            nonce=nonce,
            inbound_peers_index=inbound_peers_index,
            outbound_peers_index=outbound_peers_index,
        )

    def __hash__(self):
        return hash(
            (
                self.request,
                self.nonce,
                self.inbound_peers_index,
                self.outbound_peers_index,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.request == other.request
            and self.nonce == other.nonce
            and self.inbound_peers_index == other.inbound_peers_index
            and self.outbound_peers_index == other.outbound_peers_index
        )

    def __repr__(self):
        out = [
            f"request={self.request}",
            f"nonce={self.nonce}",
            f"inbound_peers_index={self.inbound_peers_index}",
            f"outbound_peers_index={self.outbound_peers_index}",
        ]
        return f"<TimeSlicedSurveyRequestMessage [{', '.join(out)}]>"
