# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .encrypted_body import EncryptedBody
from .node_id import NodeID
from .survey_message_command_type import SurveyMessageCommandType
from .uint32 import Uint32

__all__ = ["SurveyResponseMessage"]


class SurveyResponseMessage:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct SurveyResponseMessage
    {
        NodeID surveyorPeerID;
        NodeID surveyedPeerID;
        uint32 ledgerNum;
        SurveyMessageCommandType commandType;
        EncryptedBody encryptedBody;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        surveyor_peer_id: NodeID,
        surveyed_peer_id: NodeID,
        ledger_num: Uint32,
        command_type: SurveyMessageCommandType,
        encrypted_body: EncryptedBody,
    ) -> None:
        self.surveyor_peer_id = surveyor_peer_id
        self.surveyed_peer_id = surveyed_peer_id
        self.ledger_num = ledger_num
        self.command_type = command_type
        self.encrypted_body = encrypted_body

    def pack(self, packer: Packer) -> None:
        self.surveyor_peer_id.pack(packer)
        self.surveyed_peer_id.pack(packer)
        self.ledger_num.pack(packer)
        self.command_type.pack(packer)
        self.encrypted_body.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SurveyResponseMessage":
        surveyor_peer_id = NodeID.unpack(unpacker)
        surveyed_peer_id = NodeID.unpack(unpacker)
        ledger_num = Uint32.unpack(unpacker)
        command_type = SurveyMessageCommandType.unpack(unpacker)
        encrypted_body = EncryptedBody.unpack(unpacker)
        return cls(
            surveyor_peer_id=surveyor_peer_id,
            surveyed_peer_id=surveyed_peer_id,
            ledger_num=ledger_num,
            command_type=command_type,
            encrypted_body=encrypted_body,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SurveyResponseMessage":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SurveyResponseMessage":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.surveyor_peer_id == other.surveyor_peer_id
            and self.surveyed_peer_id == other.surveyed_peer_id
            and self.ledger_num == other.ledger_num
            and self.command_type == other.command_type
            and self.encrypted_body == other.encrypted_body
        )

    def __str__(self):
        out = [
            f"surveyor_peer_id={self.surveyor_peer_id}",
            f"surveyed_peer_id={self.surveyed_peer_id}",
            f"ledger_num={self.ledger_num}",
            f"command_type={self.command_type}",
            f"encrypted_body={self.encrypted_body}",
        ]
        return f"<SurveyResponseMessage {[', '.join(out)]}>"
