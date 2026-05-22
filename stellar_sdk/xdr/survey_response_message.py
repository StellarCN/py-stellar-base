# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .encrypted_body import EncryptedBody
from .node_id import NodeID
from .survey_message_command_type import SurveyMessageCommandType
from .uint32 import Uint32

__all__ = ["SurveyResponseMessage"]


class SurveyResponseMessage:
    """
    XDR Source Code::

        struct SurveyResponseMessage
        {
            NodeID surveyorPeerID;
            NodeID surveyedPeerID;
            uint32 ledgerNum;
            SurveyMessageCommandType commandType;
            EncryptedBody encryptedBody;
        };
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SurveyResponseMessage:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        surveyor_peer_id = NodeID.unpack(unpacker, depth_limit - 1)
        surveyed_peer_id = NodeID.unpack(unpacker, depth_limit - 1)
        ledger_num = Uint32.unpack(unpacker, depth_limit - 1)
        command_type = SurveyMessageCommandType.unpack(unpacker)
        encrypted_body = EncryptedBody.unpack(unpacker, depth_limit - 1)
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
    def from_xdr_bytes(cls, xdr: bytes) -> SurveyResponseMessage:
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
    def from_xdr(cls, xdr: str) -> SurveyResponseMessage:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SurveyResponseMessage:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "surveyor_peer_id": self.surveyor_peer_id.to_json_dict(),
            "surveyed_peer_id": self.surveyed_peer_id.to_json_dict(),
            "ledger_num": self.ledger_num.to_json_dict(),
            "command_type": self.command_type.to_json_dict(),
            "encrypted_body": self.encrypted_body.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SurveyResponseMessage:
        surveyor_peer_id = NodeID.from_json_dict(json_dict["surveyor_peer_id"])
        surveyed_peer_id = NodeID.from_json_dict(json_dict["surveyed_peer_id"])
        ledger_num = Uint32.from_json_dict(json_dict["ledger_num"])
        command_type = SurveyMessageCommandType.from_json_dict(
            json_dict["command_type"]
        )
        encrypted_body = EncryptedBody.from_json_dict(json_dict["encrypted_body"])
        return cls(
            surveyor_peer_id=surveyor_peer_id,
            surveyed_peer_id=surveyed_peer_id,
            ledger_num=ledger_num,
            command_type=command_type,
            encrypted_body=encrypted_body,
        )

    def __hash__(self):
        return hash(
            (
                self.surveyor_peer_id,
                self.surveyed_peer_id,
                self.ledger_num,
                self.command_type,
                self.encrypted_body,
            )
        )

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

    def __repr__(self):
        out = [
            f"surveyor_peer_id={self.surveyor_peer_id}",
            f"surveyed_peer_id={self.surveyed_peer_id}",
            f"ledger_num={self.ledger_num}",
            f"command_type={self.command_type}",
            f"encrypted_body={self.encrypted_body}",
        ]
        return f"<SurveyResponseMessage [{', '.join(out)}]>"
