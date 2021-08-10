from json import JSONDecodeError
from typing import Optional

from .client.response import Response

BuildInValueError = ValueError
BuildInTypeError = TypeError
BuildInAttributeError = AttributeError

__all__ = [
    "SdkError",
    "ValueError",
    "TypeError",
    "AttributeError",
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
]


class SdkError(Exception):
    """Base exception for all stellar sdk related errors"""


class ValueError(BuildInValueError, SdkError):
    """exception for all values related errors"""


class TypeError(BuildInTypeError, SdkError):
    """exception for all type related errors"""


class AttributeError(BuildInAttributeError, SdkError):
    """Attribute not found."""


class BadSignatureError(ValueError):
    """Raised when the signature was forged or otherwise corrupt."""


class Ed25519PublicKeyInvalidError(ValueError):
    """Ed25519 public key is incorrect."""


class Ed25519SecretSeedInvalidError(ValueError):
    """Ed25519 secret seed is incorrect."""


class MissingEd25519SecretSeedError(ValueError):
    """Missing Ed25519 secret seed in the keypair"""


class MuxedEd25519AccountInvalidError(ValueError):
    """Muxed Ed25519 public key is incorrect."""


class MemoInvalidException(ValueError):
    """Memo is incorrect."""


class AssetCodeInvalidError(ValueError):
    """Asset Code is incorrect."""


class AssetIssuerInvalidError(ValueError):
    """Asset issuer is incorrect."""


class NoApproximationError(SdkError):
    """Approximation cannot be found"""


class SignatureExistError(ValueError):
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

    def __str__(self):
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


def raise_request_exception(response: Response) -> None:
    status_code = response.status_code
    if status_code == 200:
        pass  # pragma: no cover
    elif status_code == 404:
        raise NotFoundError(response)
    elif 400 <= status_code < 500:
        raise BadRequestError(response)
    elif 500 <= status_code < 600:
        raise BadResponseError(response)
    else:
        raise UnknownRequestError(response)
