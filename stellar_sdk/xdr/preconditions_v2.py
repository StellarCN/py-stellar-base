# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List, Optional

from xdrlib3 import Packer, Unpacker

from .duration import Duration
from .ledger_bounds import LedgerBounds
from .sequence_number import SequenceNumber
from .signer_key import SignerKey
from .time_bounds import TimeBounds
from .uint32 import Uint32

__all__ = ["PreconditionsV2"]


class PreconditionsV2:
    """
    XDR Source Code::

        struct PreconditionsV2
        {
            TimeBounds* timeBounds;

            // Transaction only valid for ledger numbers n such that
            // minLedger <= n < maxLedger (if maxLedger == 0, then
            // only minLedger is checked)
            LedgerBounds* ledgerBounds;

            // If NULL, only valid when sourceAccount's sequence number
            // is seqNum - 1.  Otherwise, valid when sourceAccount's
            // sequence number n satisfies minSeqNum <= n < tx.seqNum.
            // Note that after execution the account's sequence number
            // is always raised to tx.seqNum, and a transaction is not
            // valid if tx.seqNum is too high to ensure replay protection.
            SequenceNumber* minSeqNum;

            // For the transaction to be valid, the current ledger time must
            // be at least minSeqAge greater than sourceAccount's seqTime.
            Duration minSeqAge;

            // For the transaction to be valid, the current ledger number
            // must be at least minSeqLedgerGap greater than sourceAccount's
            // seqLedger.
            uint32 minSeqLedgerGap;

            // For the transaction to be valid, there must be a signature
            // corresponding to every Signer in this array, even if the
            // signature is not otherwise required by the sourceAccount or
            // operations.
            SignerKey extraSigners<2>;
        };
    """

    def __init__(
        self,
        time_bounds: Optional[TimeBounds],
        ledger_bounds: Optional[LedgerBounds],
        min_seq_num: Optional[SequenceNumber],
        min_seq_age: Duration,
        min_seq_ledger_gap: Uint32,
        extra_signers: List[SignerKey],
    ) -> None:
        _expect_max_length = 2
        if extra_signers and len(extra_signers) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `extra_signers` should be {_expect_max_length}, but got {len(extra_signers)}."
            )
        self.time_bounds = time_bounds
        self.ledger_bounds = ledger_bounds
        self.min_seq_num = min_seq_num
        self.min_seq_age = min_seq_age
        self.min_seq_ledger_gap = min_seq_ledger_gap
        self.extra_signers = extra_signers

    def pack(self, packer: Packer) -> None:
        if self.time_bounds is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.time_bounds.pack(packer)
        if self.ledger_bounds is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.ledger_bounds.pack(packer)
        if self.min_seq_num is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.min_seq_num.pack(packer)
        self.min_seq_age.pack(packer)
        self.min_seq_ledger_gap.pack(packer)
        packer.pack_uint(len(self.extra_signers))
        for extra_signers_item in self.extra_signers:
            extra_signers_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> PreconditionsV2:
        time_bounds = TimeBounds.unpack(unpacker) if unpacker.unpack_uint() else None
        ledger_bounds = (
            LedgerBounds.unpack(unpacker) if unpacker.unpack_uint() else None
        )
        min_seq_num = (
            SequenceNumber.unpack(unpacker) if unpacker.unpack_uint() else None
        )
        min_seq_age = Duration.unpack(unpacker)
        min_seq_ledger_gap = Uint32.unpack(unpacker)
        length = unpacker.unpack_uint()
        extra_signers = []
        for _ in range(length):
            extra_signers.append(SignerKey.unpack(unpacker))
        return cls(
            time_bounds=time_bounds,
            ledger_bounds=ledger_bounds,
            min_seq_num=min_seq_num,
            min_seq_age=min_seq_age,
            min_seq_ledger_gap=min_seq_ledger_gap,
            extra_signers=extra_signers,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> PreconditionsV2:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> PreconditionsV2:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.time_bounds,
                self.ledger_bounds,
                self.min_seq_num,
                self.min_seq_age,
                self.min_seq_ledger_gap,
                self.extra_signers,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.time_bounds == other.time_bounds
            and self.ledger_bounds == other.ledger_bounds
            and self.min_seq_num == other.min_seq_num
            and self.min_seq_age == other.min_seq_age
            and self.min_seq_ledger_gap == other.min_seq_ledger_gap
            and self.extra_signers == other.extra_signers
        )

    def __repr__(self):
        out = [
            f"time_bounds={self.time_bounds}",
            f"ledger_bounds={self.ledger_bounds}",
            f"min_seq_num={self.min_seq_num}",
            f"min_seq_age={self.min_seq_age}",
            f"min_seq_ledger_gap={self.min_seq_ledger_gap}",
            f"extra_signers={self.extra_signers}",
        ]
        return f"<PreconditionsV2 [{', '.join(out)}]>"
