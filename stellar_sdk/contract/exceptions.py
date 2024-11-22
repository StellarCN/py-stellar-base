from typing import TYPE_CHECKING, Union

from ..exceptions import SdkError

if TYPE_CHECKING:
    from .assembled_transaction import AssembledTransaction
    from .assembled_transaction_async import AssembledTransactionAsync

__all__ = [
    "AssembledTransactionError",
    "RestorationFailureError",
    "NotYetSimulatedError",
    "SimulationFailedError",
    "ExpiredStateError",
    "NoSignatureNeededError",
    "NeedsMoreSignaturesError",
    "SendTransactionFailedError",
    "TransactionFailedError",
    "TransactionStillPendingError",
]


class AssembledTransactionError(SdkError):
    """Raised when an assembled transaction fails."""

    def __init__(
        self,
        message,
        assembled_transaction: Union[
            "AssembledTransaction", "AssembledTransactionAsync"
        ],
    ) -> None:
        super().__init__(message)
        self.assembled_transaction = assembled_transaction


class RestorationFailureError(AssembledTransactionError):
    """Raised when a restoration fails."""


class NotYetSimulatedError(AssembledTransactionError):
    """Raised when trying to get the result of a transaction that has not been simulated yet."""


class SimulationFailedError(AssembledTransactionError):
    """Raised when a simulation fails."""


class ExpiredStateError(AssembledTransactionError):
    """Raised when the state has expired."""


class NoSignatureNeededError(AssembledTransactionError):
    """Raised when no signature is needed."""


class NeedsMoreSignaturesError(AssembledTransactionError):
    """Raised when more signatures are needed."""


class SendTransactionFailedError(AssembledTransactionError):
    """Raised when invoking `send_transaction` fails."""


class TransactionFailedError(AssembledTransactionError):
    """Raised when invoking `get_transaction` fails."""


class TransactionStillPendingError(AssembledTransactionError):
    """Raised when the transaction is still pending."""
