# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .hash import Hash
from .transaction_phase import TransactionPhase

__all__ = ["TransactionSetV1"]


class TransactionSetV1:
    """
    XDR Source Code::

        struct TransactionSetV1
        {
            Hash previousLedgerHash;
            TransactionPhase phases<>;
        };
    """

    def __init__(
        self,
        previous_ledger_hash: Hash,
        phases: List[TransactionPhase],
    ) -> None:
        _expect_max_length = 4294967295
        if phases and len(phases) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `phases` should be {_expect_max_length}, but got {len(phases)}."
            )
        self.previous_ledger_hash = previous_ledger_hash
        self.phases = phases

    def pack(self, packer: Packer) -> None:
        self.previous_ledger_hash.pack(packer)
        packer.pack_uint(len(self.phases))
        for phases_item in self.phases:
            phases_item.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> TransactionSetV1:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        previous_ledger_hash = Hash.unpack(unpacker, depth_limit - 1)
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"phases length {length} exceeds remaining input length {_remaining}"
            )
        phases = []
        for _ in range(length):
            phases.append(TransactionPhase.unpack(unpacker, depth_limit - 1))
        return cls(
            previous_ledger_hash=previous_ledger_hash,
            phases=phases,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TransactionSetV1:
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
    def from_xdr(cls, xdr: str) -> TransactionSetV1:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TransactionSetV1:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "previous_ledger_hash": self.previous_ledger_hash.to_json_dict(),
            "phases": [item.to_json_dict() for item in self.phases],
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> TransactionSetV1:
        previous_ledger_hash = Hash.from_json_dict(json_dict["previous_ledger_hash"])
        phases = [TransactionPhase.from_json_dict(item) for item in json_dict["phases"]]
        return cls(
            previous_ledger_hash=previous_ledger_hash,
            phases=phases,
        )

    def __hash__(self):
        return hash(
            (
                self.previous_ledger_hash,
                self.phases,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.previous_ledger_hash == other.previous_ledger_hash
            and self.phases == other.phases
        )

    def __repr__(self):
        out = [
            f"previous_ledger_hash={self.previous_ledger_hash}",
            f"phases={self.phases}",
        ]
        return f"<TransactionSetV1 [{', '.join(out)}]>"
