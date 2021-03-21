# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .survey_message_command_type import SurveyMessageCommandType
from .topology_response_body import TopologyResponseBody
from ..exceptions import ValueError

__all__ = ["SurveyResponseBody"]


class SurveyResponseBody:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union SurveyResponseBody switch (SurveyMessageCommandType type)
    {
    case SURVEY_TOPOLOGY:
        TopologyResponseBody topologyResponseBody;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: SurveyMessageCommandType,
        topology_response_body: TopologyResponseBody = None,
    ) -> None:
        self.type = type
        self.topology_response_body = topology_response_body

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == SurveyMessageCommandType.SURVEY_TOPOLOGY:
            if self.topology_response_body is None:
                raise ValueError("topology_response_body should not be None.")
            self.topology_response_body.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SurveyResponseBody":
        type = SurveyMessageCommandType.unpack(unpacker)
        if type == SurveyMessageCommandType.SURVEY_TOPOLOGY:
            topology_response_body = TopologyResponseBody.unpack(unpacker)
            if topology_response_body is None:
                raise ValueError("topology_response_body should not be None.")
            return cls(type, topology_response_body=topology_response_body)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SurveyResponseBody":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SurveyResponseBody":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.topology_response_body == other.topology_response_body
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(
            f"topology_response_body={self.topology_response_body}"
        ) if self.topology_response_body is not None else None
        return f"<SurveyResponseBody {[', '.join(out)]}>"
