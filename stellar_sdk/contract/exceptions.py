from ..exceptions import SdkError


class RestorationFailure(SdkError):
    pass

class NotYetSimulatedError(SdkError):
    """Raised when trying to get the result of a transaction that has not been simulated yet."""

    pass


class SimulationFailedError(SdkError):
    """Raised when a simulation fails."""

    pass


class ExpiredStateError(SdkError):
    pass


class NoSignatureNeededError(SdkError):
    pass


class NeedsMoreSignaturesError(SdkError):
    pass


class SendTransactionFailedError(SdkError):
    pass


class TransactionStillPendingError(SdkError):
    pass

class TransactionAwaitingError(SdkError):
    pass

class TransactionNotSentError(SdkError):
    pass
