from ..exceptions import SdkError, BaseRequestError


class StellarTomlNotFoundError(SdkError):
    """If the SEP 0010 toml file not found, the exception will be thrown."""


class InvalidFederationAddress(SdkError):
    """If the federation address is invalid, the exception will be thrown."""


class FederationServerNotFoundError(SdkError):
    """If the federation address is invalid, the exception will be thrown."""


class BadFederationResponseError(BaseRequestError):
    """If the federation address is invalid, the exception will be thrown.

    :param response: client response
    """

    def __init__(self, response) -> None:
        super().__init__(response)
        self.message: str = response.text
        self.status: int = response.status_code


class InvalidSep10ChallengeError(SdkError):
    """If the SEP 0010 validation fails, the exception will be thrown."""
