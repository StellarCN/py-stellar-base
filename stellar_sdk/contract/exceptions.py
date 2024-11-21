from ..exceptions import SdkError


class RestorationFailureError(SdkError):
    """Raised when a restoration fails."""


class NotYetSimulatedError(SdkError):
    """Raised when trying to get the result of a transaction that has not been simulated yet."""


class SimulationFailedError(SdkError):
    """Raised when a simulation fails."""


class ExpiredStateError(SdkError):
    """Raised when the state has expired."""


class NoSignatureNeededError(SdkError):
    """Raised when no signature is needed."""


class NeedsMoreSignaturesError(SdkError):
    """Raised when more signatures are needed."""


class SendTransactionFailedError(SdkError):
    """Raised when invoking `send_transaction` fails."""


class TransactionFailedError(SdkError):
    """Raised when invoking `get_transaction` fails."""


class TransactionStillPendingError(SdkError):
    """Raised when the transaction is still pending."""
