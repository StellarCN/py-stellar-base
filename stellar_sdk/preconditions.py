from typing import List, Optional

from . import xdr as stellar_xdr
from .ledger_bounds import LedgerBounds
from .signed_payload_signer import SignedPayloadSigner
from .time_bounds import TimeBounds


class Preconditions:
    def __init__(
        self,
        time_bounds: TimeBounds = None,
        ledger_bounds: LedgerBounds = None,
        min_sequence_number: int = None,
        min_sequence_age: int = None,
        min_sequence_ledger_gap: int = None,
        extra_signers: List[SignedPayloadSigner] = None,
    ):
        self.time_bounds = time_bounds
        self.ledger_bounds = ledger_bounds
        self.min_sequence_number = min_sequence_number
        self.min_sequence_age = min_sequence_age
        self.min_sequence_ledger_gap = min_sequence_ledger_gap
        self.extra_signers = extra_signers

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.time_bounds == other.time_bounds
            and self.ledger_bounds == other.ledger_bounds
            and self.min_sequence_number == other.min_sequence_number
            and self.min_sequence_age == other.min_sequence_age
            and self.min_sequence_ledger_gap == other.min_sequence_ledger_gap
            and self.extra_signers == other.extra_signers
        )

    def to_xdr_object(self) -> stellar_xdr.Preconditions:
        """Returns the xdr object for this Preconditions object.

        :return: XDR Preconditions object
        """
        time_bounds = self.time_bounds.to_xdr_object() if self.time_bounds else None
        if (
            self.ledger_bounds is not None
            or self.min_sequence_number is not None
            or self.min_sequence_age is not None
            or self.min_sequence_ledger_gap is not None
            or self.extra_signers
        ):
            ledger_bounds = (
                self.ledger_bounds.to_xdr_object() if self.ledger_bounds else None
            )
            min_sequence_number = (
                stellar_xdr.SequenceNumber(stellar_xdr.Int64(self.min_sequence_number))
                if self.min_sequence_number is not None
                else None
            )
            min_sequence_age = (
                stellar_xdr.Duration(stellar_xdr.Int64(self.min_sequence_age))
                if self.min_sequence_age is not None
                else stellar_xdr.Duration(stellar_xdr.Int64(0))
            )
            min_sequence_ledger_gap = (
                stellar_xdr.Uint32(self.min_sequence_ledger_gap)
                if self.min_sequence_ledger_gap is not None
                else stellar_xdr.Uint32(0)
            )
            extra_signers = []
            if self.extra_signers:
                for s in self.extra_signers:
                    extra_signers.append(s.to_xdr_object())
            preconditions_v2 = stellar_xdr.PreconditionsV2(
                time_bounds=time_bounds,
                ledger_bounds=ledger_bounds,
                min_seq_num=min_sequence_number,
                min_seq_age=min_sequence_age,
                min_seq_ledger_gap=min_sequence_ledger_gap,
                extra_signers=extra_signers,
            )
            preconditions = stellar_xdr.Preconditions(
                stellar_xdr.PreconditionType.PRECOND_V2,
                v2=preconditions_v2,
            )
        elif time_bounds:
            preconditions = stellar_xdr.Preconditions(
                stellar_xdr.PreconditionType.PRECOND_TIME, time_bounds=time_bounds
            )
        else:
            preconditions = stellar_xdr.Preconditions(
                stellar_xdr.PreconditionType.PRECOND_NONE
            )
        return preconditions

    @classmethod
    def from_xdr_object(cls, xdr_object: stellar_xdr.Preconditions) -> "Preconditions":
        """Create a :class:`Preconditions` from an XDR Preconditions object.

        :param xdr_object: The XDR LedgerBounds object.
        :return: A new :class:`LedgerBounds` object from the given XDR LedgerBounds object.
        """

        if xdr_object.type == stellar_xdr.PreconditionType.PRECOND_V2:
            assert xdr_object.v2 is not None
            time_bounds = (
                TimeBounds.from_xdr_object(xdr_object.v2.time_bounds)
                if xdr_object.v2.time_bounds
                else None
            )
            ledger_bounds = (
                LedgerBounds.from_xdr_object(xdr_object.v2.ledger_bounds)
                if xdr_object.v2.ledger_bounds
                else None
            )
            # min_sequence_number is nullable
            min_sequence_number = (
                xdr_object.v2.min_seq_num.sequence_number.int64
                if xdr_object.v2.min_seq_num is not None
                else None
            )
            min_sequence_age = (
                xdr_object.v2.min_seq_age.duration.int64
                if xdr_object.v2.min_seq_age
                else None
            )
            min_sequence_ledger_gap = (
                xdr_object.v2.min_seq_ledger_gap.uint32
                if xdr_object.v2.min_seq_ledger_gap
                else None
            )
            if xdr_object.v2.extra_signers:
                extra_signers: Optional[List[SignedPayloadSigner]] = [
                    SignedPayloadSigner.from_xdr_object(s)
                    for s in xdr_object.v2.extra_signers
                ]
            else:
                extra_signers = None
            return cls(
                time_bounds=time_bounds,
                ledger_bounds=ledger_bounds,
                min_sequence_number=min_sequence_number,
                min_sequence_age=min_sequence_age,
                min_sequence_ledger_gap=min_sequence_ledger_gap,
                extra_signers=extra_signers,
            )
        elif xdr_object.type == stellar_xdr.PreconditionType.PRECOND_TIME:
            time_bounds = (
                TimeBounds.from_xdr_object(xdr_object.time_bounds)
                if xdr_object.time_bounds
                else None
            )
            return cls(time_bounds=time_bounds)
        elif xdr_object.type == stellar_xdr.PreconditionType.PRECOND_NONE:
            return cls()
        else:
            raise ValueError("Invalid Preconditions type.")

    def __str__(self):
        return (
            f"<Preconditions ["
            f"time_bounds={self.time_bounds}, "
            f"ledger_bounds={self.ledger_bounds}, "
            f"min_sequence_number={self.min_sequence_number}, "
            f"min_sequence_age={self.min_sequence_age}, "
            f"min_sequence_ledger_gap={self.min_sequence_ledger_gap}, "
            f"extra_signers={self.extra_signers}"
            f"]>"
        )
