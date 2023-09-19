"""
SEP: 0035
Title: Operation IDs
Author: Scott Fleckenstein (@nullstyle), Isaiah Turner (@Isaiah-Turner), Debnil Sur (@debnil)
Track: Standard
Status: Draft
Created: 2020-08-26
Discussion: https://groups.google.com/g/stellar-dev/c/vCgQhmox32Q
"""

__all__ = ["TOID"]

from typing import Tuple


class TOID:
    """TOID represents the total order of Ledgers, Transactions and Operations.
    This is an implementation of SEP-35: https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0035.md

    Operations within the stellar network have a total order, expressed by three
    pieces of information: the ledger sequence the operation was validated in,
    the order which the operation's containing transaction was applied in
    that ledger, and the index of the operation within that parent transaction.

    :param ledger_sequence: The ledger sequence the operation was validated in.
    :param transaction_order: The order that the transaction was applied within the ledger where it was validated.
        The application order value starts at 1. The maximum supported number of transactions
        per operation is 1,048,575.
    :param operation_order: The index of the operation within that parent transaction. The operation index value
        starts at 1. The maximum supported number of operations per transaction is 4095.
    """

    def __init__(
        self, ledger_sequence: int, transaction_order: int, operation_order: int
    ) -> None:
        if ledger_sequence < 0 or ledger_sequence > 2**31 - 1:
            raise ValueError(
                "Invalid `ledger_sequence`, it must be between 0 and 2147483647."
            )

        if transaction_order < 0 or transaction_order > 2**20 - 1:
            raise ValueError(
                "Invalid `transaction_order`, it must be between 0 and 1048575."
            )

        if operation_order < 0 or operation_order > 2**12 - 1:
            raise ValueError(
                "Invalid `operation_order`, it must be between 0 and 4095."
            )

        self.ledger_sequence = ledger_sequence
        self.transaction_order = transaction_order
        self.operation_order = operation_order

    def to_int64(self) -> int:
        """Converts the TOID to a signed 64-bit integer.

        :return: The signed 64-bit integer representation of the TOID.
        """
        return (
            self.ledger_sequence << 32
            | self.transaction_order << 12
            | self.operation_order
        )

    @classmethod
    def from_int64(cls, value: int) -> "TOID":
        """Converts a signed 64-bit integer to a TOID.

        :param value: The signed 64-bit integer to convert.
        """
        if value < 0 or value > 2**63 - 1:
            raise ValueError(
                "Invalid `value`, it must be between 0 and 9223372036854775807."
            )
        return TOID(value >> 32, (value >> 12) & 0xFFFFF, value & 0xFFF)

    def increment_operation_order(self) -> None:
        """Increments the operation order by 1, rolling over to the next ledger if overflow occurs.
        This allows queries to easily advance a cursor to the next operation.

        :return: The current TOID instance.
        """
        if self.operation_order == 2**12 - 1:
            self.operation_order = 0
            self.ledger_sequence += 1
        else:
            self.operation_order += 1

    @classmethod
    def after_ledger(cls, ledger_sequence: int) -> "TOID":
        """Creates a new toid that represents the ledger time **after** any
        contents (e.g. transactions, operations) that occur within the specified ledger.

        :param ledger_sequence: The ledger sequence.
        :return: The TOID instance.
        """
        return TOID(ledger_sequence, 2**20 - 1, 2**12 - 1)

    @staticmethod
    def ledger_range_inclusive(start: int, end: int) -> Tuple[int, int]:
        """The inclusive range representation between two
        ledgers inclusive. The second value points at the end+1 ledger so when using
        this value make sure < order is used.

        :param start: The start ledger sequence.
        :param end: The end ledger sequence.
        :return: The inclusive range representation between two ledgers.
        """
        if start > end:
            raise ValueError(
                "Invalid `start` and `end` values, `start` must be less than or equal to `end`."
            )
        toid_start = 0
        if start != 1:
            toid_start = TOID(start, 0, 0).to_int64()
        toid_end = TOID(end + 1, 0, 0).to_int64()
        return toid_start, toid_end

    def __hash__(self):
        return hash(
            (self.ledger_sequence, self.transaction_order, self.operation_order)
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ledger_sequence == other.ledger_sequence
            and self.transaction_order == other.transaction_order
            and self.operation_order == other.operation_order
        )

    def __repr__(self) -> str:
        return (
            f"<TOID [ledger_sequence={self.ledger_sequence}, "
            f"transaction_order={self.transaction_order}, "
            f"operation_order={self.operation_order}]>"
        )
