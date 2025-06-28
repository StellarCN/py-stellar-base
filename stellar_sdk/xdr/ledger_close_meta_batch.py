# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

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
    def unpack(cls, unpacker: Unpacker) -> LedgerCloseMetaBatch:
        start_sequence = Uint32.unpack(unpacker)
        end_sequence = Uint32.unpack(unpacker)
        length = unpacker.unpack_uint()
        ledger_close_metas = []
        for _ in range(length):
            ledger_close_metas.append(LedgerCloseMeta.unpack(unpacker))
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
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LedgerCloseMetaBatch:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
