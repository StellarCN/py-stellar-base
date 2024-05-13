from typing import List, Optional, Sequence

from . import xdr as stellar_xdr
from .ledger_bounds import LedgerBounds
from .signer_key import SignerKey
from .time_bounds import TimeBounds


class Preconditions:
    """This contains a set of conditions, if a transaction can be accepted by the network,
    it must meet these conditions.

    :param time_bounds: The timebounds for the transaction.
    :param ledger_bounds: The ledgerbounds for the transaction.
    :param min_sequence_number: The minimum source account sequence
        number this transaction is valid for. If the value is ``None``,
        the transaction is valid when **source account's sequence number == tx.sequence - 1**.
    :param min_sequence_age: The minimum amount of time between
        source account sequence time and the ledger time when this transaction
        will become valid. If the value is ``0`` or ``None``, the transaction is unrestricted
        by the account sequence age. Cannot be negative.
    :param min_sequence_ledger_gap: The minimum number of ledgers between source account
        sequence and the ledger number when this transaction will become valid.
        If the value is ``0`` or ``None``, the transaction is unrestricted by the account sequence
        ledger. Cannot be negative.
    :param extra_signers: required extra signers.
    """

    def __init__(
        self,
        time_bounds: TimeBounds = None,
        ledger_bounds: LedgerBounds = None,
        min_sequence_number: int = None,
        min_sequence_age: int = None,
        min_sequence_ledger_gap: int = None,
        extra_signers: Sequence[SignerKey] = None,
    ):
        if not extra_signers:
            extra_signers = []

        if len(extra_signers) > 2:
            raise ValueError('"extra_signers" cannot be longer than 2 elements.')

        self.time_bounds = time_bounds
        self.ledger_bounds = ledger_bounds
        self.min_sequence_number = min_sequence_number
        self.min_sequence_age = min_sequence_age
        self.min_sequence_ledger_gap = min_sequence_ledger_gap
        self.extra_signers = extra_signers

        if self._is_v2():
            self.min_sequence_age = (
                0 if self.min_sequence_age is None else self.min_sequence_age
            )
            self.min_sequence_ledger_gap = (
                0
                if self.min_sequence_ledger_gap is None
                else self.min_sequence_ledger_gap
            )

    def _is_empty_preconditions(self) -> bool:
        return not (
            self.time_bounds
            or self.ledger_bounds
            or self.min_sequence_number is not None
            or self.min_sequence_age is not None
            or self.min_sequence_ledger_gap is not None
            or self.extra_signers
        )

    def _is_v2(self) -> bool:
        return bool(
            self.ledger_bounds
            or self.min_sequence_number is not None
            or self.min_sequence_age is not None
            or self.min_sequence_ledger_gap is not None
            or self.extra_signers
        )

    def to_xdr_object(self) -> stellar_xdr.Preconditions:
        """Returns the xdr object for this Preconditions object.

        :return: XDR Preconditions object
        """
        time_bounds = self.time_bounds.to_xdr_object() if self.time_bounds else None
        if self._is_v2():
            ledger_bounds = (
                self.ledger_bounds.to_xdr_object() if self.ledger_bounds else None
            )
            min_sequence_number = (
                stellar_xdr.SequenceNumber(stellar_xdr.Int64(self.min_sequence_number))
                if self.min_sequence_number is not None
                else None
            )
            min_sequence_age = (
                stellar_xdr.Duration(stellar_xdr.Uint64(self.min_sequence_age))
                if self.min_sequence_age is not None
                else stellar_xdr.Duration(stellar_xdr.Uint64(0))
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
            min_sequence_age = xdr_object.v2.min_seq_age.duration.uint64
            min_sequence_ledger_gap = xdr_object.v2.min_seq_ledger_gap.uint32
            extra_signers: Optional[List[SignerKey]] = [
                SignerKey.from_xdr_object(s) for s in xdr_object.v2.extra_signers
            ]
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
            raise ValueError(f"Invalid PreconditionType: {xdr_object.type!r}")

    def __hash__(self):
        return hash(
            (
                self.time_bounds,
                self.ledger_bounds,
                self.min_sequence_number,
                self.min_sequence_age,
                self.min_sequence_ledger_gap,
                self.extra_signers,
            )
        )

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

    def __repr__(self):
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
