from json import JSONDecodeError
from typing import Optional

from .client.response import Response

__all__ = [
    "SdkError",
    "BadSignatureError",
    "Ed25519PublicKeyInvalidError",
    "Ed25519SecretSeedInvalidError",
    "MissingEd25519SecretSeedError",
    "MuxedEd25519AccountInvalidError",
    "MemoInvalidException",
    "AssetCodeInvalidError",
    "AssetIssuerInvalidError",
    "NoApproximationError",
    "SignatureExistError",
    "BaseRequestError",
    "BaseHorizonError",
    "ConnectionError",
    "NotFoundError",
    "BadRequestError",
    "BadResponseError",
    "UnknownRequestError",
    "NotPageableError",
    "StreamClientError",
    "FeatureNotEnabledError",
    "SorobanRpcErrorResponse",
    "AccountNotFoundException",
    "PrepareTransactionException",
]

from .soroban_rpc import SimulateTransactionResponse


class SdkError(Exception):
    """Base exception for all stellar sdk related errors"""


class BadSignatureError(SdkError, ValueError):
    """Raised when the signature was forged or otherwise corrupt."""


class Ed25519PublicKeyInvalidError(SdkError, ValueError):
    """Ed25519 public key is incorrect."""


class Ed25519SecretSeedInvalidError(SdkError, ValueError):
    """Ed25519 secret seed is incorrect."""


class MissingEd25519SecretSeedError(SdkError, ValueError):
    """Missing Ed25519 secret seed in the keypair"""


class MuxedEd25519AccountInvalidError(SdkError, ValueError):
    """Muxed Ed25519 public key is incorrect."""


class MemoInvalidException(SdkError, ValueError):
    """Memo is incorrect."""


class AssetCodeInvalidError(SdkError, ValueError):
    """Asset Code is incorrect."""


class AssetIssuerInvalidError(SdkError, ValueError):
    """Asset issuer is incorrect."""


class NoApproximationError(SdkError):
    """Approximation cannot be found"""


class SignatureExistError(SdkError, ValueError):
    """A keypair can only sign a transaction once."""


class BaseRequestError(SdkError):
    """Base class for requests errors."""


class ConnectionError(BaseRequestError):
    """Base class for client connection errors."""


class BaseHorizonError(BaseRequestError):
    """Base class for horizon request errors.

    :param response: client response
    """

    def __init__(self, response: Response) -> None:
        super().__init__(response)

        self.message: str = response.text
        self.status: int = response.status_code

        message = {}
        try:
            message = response.json()
        except JSONDecodeError:
            pass  # pragma: no cover
        self.type: Optional[str] = message.get("type")
        self.title: Optional[str] = message.get("title")
        self.detail: Optional[str] = message.get("detail")
        self.extras: Optional[dict] = message.get("extras")
        self.result_xdr: Optional[str] = message.get("extras", {}).get("result_xdr")

    def __repr__(self):
        return self.message


class NotFoundError(BaseHorizonError):
    """This exception is thrown when the requested resource does not exist.
    status_code == 400

    """

    def __init__(self, response):
        super().__init__(response)


class BadRequestError(BaseHorizonError):
    """The request from the client has an error.
    400 <= status_code < 500 and status_code != 404

    """

    def __init__(self, response):
        super().__init__(response)


class BadResponseError(BaseHorizonError):
    """The response from the server has an error.
    500 <= status_code < 600


    """

    def __init__(self, response):
        super().__init__(response)


class UnknownRequestError(BaseHorizonError):
    """Unknown request exception, please create an issue feedback for this issue."""


class NotPageableError(BaseRequestError):
    """There is no previous or next page"""


class StreamClientError(BaseRequestError):
    """Failed to fetch stream resource.

    :param current_cursor: The cursor of the last message obtained can be used for reconnect.
    :param message: error message
    """

    def __init__(self, current_cursor: str, message: str) -> None:
        super().__init__(message)
        self.current_cursor = current_cursor


class FeatureNotEnabledError(SdkError):
    """The feature is not enabled."""


class SorobanRpcErrorResponse(BaseRequestError):
    """The exception is thrown when the RPC server returns an error response."""

    def __init__(
        self, code: int, message: Optional[str], data: Optional[str] = None
    ) -> None:
        super().__init__(message)
        self.code = code
        self.data = data
        self.message = message


class AccountNotFoundException(SdkError):
    """The exception is thrown when trying to load an account that doesn't exist on the Stellar network."""

    def __init__(self, account_id: str) -> None:
        super().__init__(f"Account not found, account_id: {account_id}")
        self.account_id = account_id


class PrepareTransactionException(SdkError):
    """The exception is thrown when trying to prepare a transaction."""

    def __init__(
        self, message: str, simulate_transaction_response: SimulateTransactionResponse
    ) -> None:
        super().__init__(message)
        self.message = message
        self.simulate_transaction_response = simulate_transaction_response


def raise_request_exception(response: Response) -> None:
    status_code = response.status_code
    if 200 <= status_code < 300:
        pass  # pragma: no cover
    elif status_code == 404:
        raise NotFoundError(response)
    elif 400 <= status_code < 500:
        raise BadRequestError(response)
    elif 500 <= status_code < 600:
        raise BadResponseError(response)
    else:
        raise UnknownRequestError(response)
