from ..exceptions import SdkError


class StellarTomlNotFoundError(SdkError):
    """If the SEP 0010 toml file not found, the exception will be thrown."""


class InvalidSep10ChallengeError(SdkError):
    """If the SEP 0010 validation fails, the exception will be thrown."""
