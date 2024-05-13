# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .curve25519_public import Curve25519Public
from .node_id import NodeID
from .survey_message_command_type import SurveyMessageCommandType
from .uint32 import Uint32

__all__ = ["SurveyRequestMessage"]


class SurveyRequestMessage:
    """
    XDR Source Code::

        struct SurveyRequestMessage
        {
            NodeID surveyorPeerID;
            NodeID surveyedPeerID;
            uint32 ledgerNum;
            Curve25519Public encryptionKey;
            SurveyMessageCommandType commandType;
        };
    """

    def __init__(
        self,
        surveyor_peer_id: NodeID,
        surveyed_peer_id: NodeID,
        ledger_num: Uint32,
        encryption_key: Curve25519Public,
        command_type: SurveyMessageCommandType,
    ) -> None:
        self.surveyor_peer_id = surveyor_peer_id
        self.surveyed_peer_id = surveyed_peer_id
        self.ledger_num = ledger_num
        self.encryption_key = encryption_key
        self.command_type = command_type

    def pack(self, packer: Packer) -> None:
        self.surveyor_peer_id.pack(packer)
        self.surveyed_peer_id.pack(packer)
        self.ledger_num.pack(packer)
        self.encryption_key.pack(packer)
        self.command_type.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SurveyRequestMessage:
        surveyor_peer_id = NodeID.unpack(unpacker)
        surveyed_peer_id = NodeID.unpack(unpacker)
        ledger_num = Uint32.unpack(unpacker)
        encryption_key = Curve25519Public.unpack(unpacker)
        command_type = SurveyMessageCommandType.unpack(unpacker)
        return cls(
            surveyor_peer_id=surveyor_peer_id,
            surveyed_peer_id=surveyed_peer_id,
            ledger_num=ledger_num,
            encryption_key=encryption_key,
            command_type=command_type,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SurveyRequestMessage:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SurveyRequestMessage:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.surveyor_peer_id,
                self.surveyed_peer_id,
                self.ledger_num,
                self.encryption_key,
                self.command_type,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.surveyor_peer_id == other.surveyor_peer_id
            and self.surveyed_peer_id == other.surveyed_peer_id
            and self.ledger_num == other.ledger_num
            and self.encryption_key == other.encryption_key
            and self.command_type == other.command_type
        )

    def __repr__(self):
        out = [
            f"surveyor_peer_id={self.surveyor_peer_id}",
            f"surveyed_peer_id={self.surveyed_peer_id}",
            f"ledger_num={self.ledger_num}",
            f"encryption_key={self.encryption_key}",
            f"command_type={self.command_type}",
        ]
        return f"<SurveyRequestMessage [{', '.join(out)}]>"
