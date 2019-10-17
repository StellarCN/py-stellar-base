from ..exceptions import SdkError


class InvalidSep10ChallengeError(SdkError):
    """If the SEP 0010 validation fails, the exception will be thrown."""
