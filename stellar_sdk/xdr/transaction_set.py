# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .hash import Hash
from .transaction_envelope import TransactionEnvelope

__all__ = ["TransactionSet"]


class TransactionSet:
    """
    XDR Source Code::

        struct TransactionSet
        {
            Hash previousLedgerHash;
            TransactionEnvelope txs<>;
        };
    """

    def __init__(
        self,
        previous_ledger_hash: Hash,
        txs: List[TransactionEnvelope],
    ) -> None:
        _expect_max_length = 4294967295
        if txs and len(txs) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `txs` should be {_expect_max_length}, but got {len(txs)}."
            )
        self.previous_ledger_hash = previous_ledger_hash
        self.txs = txs

    def pack(self, packer: Packer) -> None:
        self.previous_ledger_hash.pack(packer)
        packer.pack_uint(len(self.txs))
        for txs_item in self.txs:
            txs_item.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> TransactionSet:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        previous_ledger_hash = Hash.unpack(unpacker, depth_limit - 1)
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"txs length {length} exceeds remaining input length {_remaining}"
            )
        txs = []
        for _ in range(length):
            txs.append(TransactionEnvelope.unpack(unpacker, depth_limit - 1))
        return cls(
            previous_ledger_hash=previous_ledger_hash,
            txs=txs,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TransactionSet:
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
    def from_xdr(cls, xdr: str) -> TransactionSet:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TransactionSet:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "previous_ledger_hash": self.previous_ledger_hash.to_json_dict(),
            "txs": [item.to_json_dict() for item in self.txs],
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> TransactionSet:
        previous_ledger_hash = Hash.from_json_dict(json_dict["previous_ledger_hash"])
        txs = [TransactionEnvelope.from_json_dict(item) for item in json_dict["txs"]]
        return cls(
            previous_ledger_hash=previous_ledger_hash,
            txs=txs,
        )

    def __hash__(self):
        return hash(
            (
                self.previous_ledger_hash,
                self.txs,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.previous_ledger_hash == other.previous_ledger_hash
            and self.txs == other.txs
        )

    def __repr__(self):
        out = [
            f"previous_ledger_hash={self.previous_ledger_hash}",
            f"txs={self.txs}",
        ]
        return f"<TransactionSet [{', '.join(out)}]>"
