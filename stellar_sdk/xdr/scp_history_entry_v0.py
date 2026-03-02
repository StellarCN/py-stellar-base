# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .ledger_scp_messages import LedgerSCPMessages
from .scp_quorum_set import SCPQuorumSet

__all__ = ["SCPHistoryEntryV0"]


class SCPHistoryEntryV0:
    """
    XDR Source Code::

        struct SCPHistoryEntryV0
        {
            SCPQuorumSet quorumSets<>; // additional quorum sets used by ledgerMessages
            LedgerSCPMessages ledgerMessages;
        };
    """

    def __init__(
        self,
        quorum_sets: List[SCPQuorumSet],
        ledger_messages: LedgerSCPMessages,
    ) -> None:
        _expect_max_length = 4294967295
        if quorum_sets and len(quorum_sets) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `quorum_sets` should be {_expect_max_length}, but got {len(quorum_sets)}."
            )
        self.quorum_sets = quorum_sets
        self.ledger_messages = ledger_messages

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.quorum_sets))
        for quorum_sets_item in self.quorum_sets:
            quorum_sets_item.pack(packer)
        self.ledger_messages.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCPHistoryEntryV0:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"quorum_sets length {length} exceeds remaining input length {_remaining}"
            )
        quorum_sets = []
        for _ in range(length):
            quorum_sets.append(SCPQuorumSet.unpack(unpacker, depth_limit - 1))
        ledger_messages = LedgerSCPMessages.unpack(unpacker, depth_limit - 1)
        return cls(
            quorum_sets=quorum_sets,
            ledger_messages=ledger_messages,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCPHistoryEntryV0:
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
    def from_xdr(cls, xdr: str) -> SCPHistoryEntryV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCPHistoryEntryV0:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "quorum_sets": [item.to_json_dict() for item in self.quorum_sets],
            "ledger_messages": self.ledger_messages.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SCPHistoryEntryV0:
        quorum_sets = [
            SCPQuorumSet.from_json_dict(item) for item in json_dict["quorum_sets"]
        ]
        ledger_messages = LedgerSCPMessages.from_json_dict(json_dict["ledger_messages"])
        return cls(
            quorum_sets=quorum_sets,
            ledger_messages=ledger_messages,
        )

    def __hash__(self):
        return hash(
            (
                self.quorum_sets,
                self.ledger_messages,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.quorum_sets == other.quorum_sets
            and self.ledger_messages == other.ledger_messages
        )

    def __repr__(self):
        out = [
            f"quorum_sets={self.quorum_sets}",
            f"ledger_messages={self.ledger_messages}",
        ]
        return f"<SCPHistoryEntryV0 [{', '.join(out)}]>"
