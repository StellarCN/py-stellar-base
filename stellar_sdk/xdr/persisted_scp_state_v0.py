# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

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
    def unpack(cls, unpacker: Unpacker) -> PersistedSCPStateV0:
        length = unpacker.unpack_uint()
        scp_envelopes = []
        for _ in range(length):
            scp_envelopes.append(SCPEnvelope.unpack(unpacker))
        length = unpacker.unpack_uint()
        quorum_sets = []
        for _ in range(length):
            quorum_sets.append(SCPQuorumSet.unpack(unpacker))
        length = unpacker.unpack_uint()
        tx_sets = []
        for _ in range(length):
            tx_sets.append(StoredTransactionSet.unpack(unpacker))
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
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> PersistedSCPStateV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
