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


class AccountRequiresMemoError(SdkError):
    """AccountRequiresMemoError is raised when a transaction is trying to submit an
    operation to an account which requires a memo.

    This error contains two attributes to help you identify the account requiring
    the memo and the operation where the account is the destination.

    See `SEP-0029 <https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0029.md>`_ for more
    information.
    """

    def __init__(self, message, account_id, operation_index) -> None:
        super().__init__(message)
        self.account_id: str = account_id
        self.operation_index: int = operation_index
