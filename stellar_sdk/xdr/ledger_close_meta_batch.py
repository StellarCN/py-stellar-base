# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .ledger_close_meta import LedgerCloseMeta
from .uint32 import Uint32

__all__ = ["LedgerCloseMetaBatch"]


class LedgerCloseMetaBatch:
    """
    XDR Source Code::

        struct LedgerCloseMetaBatch
        {
            // starting ledger sequence number in the batch
            uint32 startSequence;

            // ending ledger sequence number in the batch
            uint32 endSequence;

            // Ledger close meta for each ledger within the batch
            LedgerCloseMeta ledgerCloseMetas<>;
        };
    """

    def __init__(
        self,
        start_sequence: Uint32,
        end_sequence: Uint32,
        ledger_close_metas: List[LedgerCloseMeta],
    ) -> None:
        _expect_max_length = 4294967295
        if ledger_close_metas and len(ledger_close_metas) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `ledger_close_metas` should be {_expect_max_length}, but got {len(ledger_close_metas)}."
            )
        self.start_sequence = start_sequence
        self.end_sequence = end_sequence
        self.ledger_close_metas = ledger_close_metas

    def pack(self, packer: Packer) -> None:
        self.start_sequence.pack(packer)
        self.end_sequence.pack(packer)
        packer.pack_uint(len(self.ledger_close_metas))
        for ledger_close_metas_item in self.ledger_close_metas:
            ledger_close_metas_item.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> LedgerCloseMetaBatch:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        start_sequence = Uint32.unpack(unpacker, depth_limit - 1)
        end_sequence = Uint32.unpack(unpacker, depth_limit - 1)
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"ledger_close_metas length {length} exceeds remaining input length {_remaining}"
            )
        ledger_close_metas = []
        for _ in range(length):
            ledger_close_metas.append(LedgerCloseMeta.unpack(unpacker, depth_limit - 1))
        return cls(
            start_sequence=start_sequence,
            end_sequence=end_sequence,
            ledger_close_metas=ledger_close_metas,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerCloseMetaBatch:
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
    def from_xdr(cls, xdr: str) -> LedgerCloseMetaBatch:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LedgerCloseMetaBatch:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "start_sequence": self.start_sequence.to_json_dict(),
            "end_sequence": self.end_sequence.to_json_dict(),
            "ledger_close_metas": [
                item.to_json_dict() for item in self.ledger_close_metas
            ],
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> LedgerCloseMetaBatch:
        start_sequence = Uint32.from_json_dict(json_dict["start_sequence"])
        end_sequence = Uint32.from_json_dict(json_dict["end_sequence"])
        ledger_close_metas = [
            LedgerCloseMeta.from_json_dict(item)
            for item in json_dict["ledger_close_metas"]
        ]
        return cls(
            start_sequence=start_sequence,
            end_sequence=end_sequence,
            ledger_close_metas=ledger_close_metas,
        )

    def __hash__(self):
        return hash(
            (
                self.start_sequence,
                self.end_sequence,
                self.ledger_close_metas,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.start_sequence == other.start_sequence
            and self.end_sequence == other.end_sequence
            and self.ledger_close_metas == other.ledger_close_metas
        )

    def __repr__(self):
        out = [
            f"start_sequence={self.start_sequence}",
            f"end_sequence={self.end_sequence}",
            f"ledger_close_metas={self.ledger_close_metas}",
        ]
        return f"<LedgerCloseMetaBatch [{', '.join(out)}]>"
