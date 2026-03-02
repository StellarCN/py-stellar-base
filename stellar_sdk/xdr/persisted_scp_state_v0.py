# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .scp_envelope import SCPEnvelope
from .scp_quorum_set import SCPQuorumSet
from .stored_transaction_set import StoredTransactionSet

__all__ = ["PersistedSCPStateV0"]


class PersistedSCPStateV0:
    """
    XDR Source Code::

                                                                struct PersistedSCPStateV0
                                                                {
                                                                        SCPEnvelope scpEnvelopes<>;
                                                                        SCPQuorumSet quorumSets<>;
                                                                        StoredTransactionSet txSets<>;
                                                                };
    """

    def __init__(
        self,
        scp_envelopes: List[SCPEnvelope],
        quorum_sets: List[SCPQuorumSet],
        tx_sets: List[StoredTransactionSet],
    ) -> None:
        _expect_max_length = 4294967295
        if scp_envelopes and len(scp_envelopes) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `scp_envelopes` should be {_expect_max_length}, but got {len(scp_envelopes)}."
            )
        _expect_max_length = 4294967295
        if quorum_sets and len(quorum_sets) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `quorum_sets` should be {_expect_max_length}, but got {len(quorum_sets)}."
            )
        _expect_max_length = 4294967295
        if tx_sets and len(tx_sets) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `tx_sets` should be {_expect_max_length}, but got {len(tx_sets)}."
            )
        self.scp_envelopes = scp_envelopes
        self.quorum_sets = quorum_sets
        self.tx_sets = tx_sets

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.scp_envelopes))
        for scp_envelopes_item in self.scp_envelopes:
            scp_envelopes_item.pack(packer)
        packer.pack_uint(len(self.quorum_sets))
        for quorum_sets_item in self.quorum_sets:
            quorum_sets_item.pack(packer)
        packer.pack_uint(len(self.tx_sets))
        for tx_sets_item in self.tx_sets:
            tx_sets_item.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> PersistedSCPStateV0:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"scp_envelopes length {length} exceeds remaining input length {_remaining}"
            )
        scp_envelopes = []
        for _ in range(length):
            scp_envelopes.append(SCPEnvelope.unpack(unpacker, depth_limit - 1))
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"quorum_sets length {length} exceeds remaining input length {_remaining}"
            )
        quorum_sets = []
        for _ in range(length):
            quorum_sets.append(SCPQuorumSet.unpack(unpacker, depth_limit - 1))
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"tx_sets length {length} exceeds remaining input length {_remaining}"
            )
        tx_sets = []
        for _ in range(length):
            tx_sets.append(StoredTransactionSet.unpack(unpacker, depth_limit - 1))
        return cls(
            scp_envelopes=scp_envelopes,
            quorum_sets=quorum_sets,
            tx_sets=tx_sets,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> PersistedSCPStateV0:
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
    def from_xdr(cls, xdr: str) -> PersistedSCPStateV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> PersistedSCPStateV0:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "scp_envelopes": [item.to_json_dict() for item in self.scp_envelopes],
            "quorum_sets": [item.to_json_dict() for item in self.quorum_sets],
            "tx_sets": [item.to_json_dict() for item in self.tx_sets],
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> PersistedSCPStateV0:
        scp_envelopes = [
            SCPEnvelope.from_json_dict(item) for item in json_dict["scp_envelopes"]
        ]
        quorum_sets = [
            SCPQuorumSet.from_json_dict(item) for item in json_dict["quorum_sets"]
        ]
        tx_sets = [
            StoredTransactionSet.from_json_dict(item) for item in json_dict["tx_sets"]
        ]
        return cls(
            scp_envelopes=scp_envelopes,
            quorum_sets=quorum_sets,
            tx_sets=tx_sets,
        )

    def __hash__(self):
        return hash(
            (
                self.scp_envelopes,
                self.quorum_sets,
                self.tx_sets,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.scp_envelopes == other.scp_envelopes
            and self.quorum_sets == other.quorum_sets
            and self.tx_sets == other.tx_sets
        )

    def __repr__(self):
        out = [
            f"scp_envelopes={self.scp_envelopes}",
            f"quorum_sets={self.quorum_sets}",
            f"tx_sets={self.tx_sets}",
        ]
        return f"<PersistedSCPStateV0 [{', '.join(out)}]>"
