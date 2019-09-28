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
    "MemoInvalidException",
    "AssetCodeInvalidError",
    "AssetIssuerInvalidError",
    "NoApproximationError",
    "SignatureExistError",
    "BaseRequestError",
    "ConnectionError",
    "NotFoundError",
    "BadRequestError",
    "BadResponseError",
    "UnknownRequestError",
    "NotPageableError",
]


class SdkError(Exception):
    """Base exception for all stellar sdk related errors
    """


class ValueError(BuildInValueError, SdkError):
    """exception for all values related errors

    """


class TypeError(BuildInTypeError, SdkError):
    """exception for all type related errors

    """


class AttributeError(BuildInAttributeError, SdkError):
    """ Attribute not found. """


class BadSignatureError(ValueError):
    """Raised when the signature was forged or otherwise corrupt.
    """


class Ed25519PublicKeyInvalidError(ValueError):
    """Ed25519 public key is incorrect.

    """


class Ed25519SecretSeedInvalidError(ValueError):
    """Ed25519 secret seed is incorrect.

    """


class MissingEd25519SecretSeedError(ValueError):
    """Missing Ed25519 secret seed in the keypair

    """


class MemoInvalidException(ValueError):
    """Memo is incorrect.

    """


class AssetCodeInvalidError(ValueError):
    """Asset Code is incorrect.

    """


class AssetIssuerInvalidError(ValueError):
    """Asset issuer is incorrect.

    """


class NoApproximationError(SdkError):
    """Approximation cannot be found

    """


class SignatureExistError(ValueError):
    """A keypair can only sign a transaction once.

    """


class BaseRequestError(SdkError):
    """Base class for requests errors.
    """


class ConnectionError(BaseRequestError):
    """Base class for client connection errors.

    """


class BaseHorizonError(BaseRequestError):
    """Base class for horizon request errors.

    :param response: client response
    """

    def __init__(self, response: Response) -> None:
        super().__init__(response)
        message = response.json()
        self.type = message.get("type")
        self.title = message.get("title")
        self.status = message.get("status")
        self.detail = message.get("detail")
        self.extras = message.get("extras")

    def __str__(self):
        return """\n\ttype: {type}
        title: {title}
        status: {status}
        detail: {detail}
        extras: {extras}
        """.format(
            type=self.type,
            title=self.title,
            status=self.status,
            detail=self.detail,
            extras=self.extras,
        )


class NotFoundError(BaseHorizonError):
    """This exception is thrown when the requested resource does not exist.

    """

    def __init__(self, response):
        super().__init__(response)


class BadRequestError(BaseHorizonError):
    """The request from the client has an error.

    """

    def __init__(self, response):
        super().__init__(response)


class BadResponseError(BaseHorizonError):
    """The response from the server has an error.

    """

    def __init__(self, response):
        super().__init__(response)


class UnknownRequestError(BaseHorizonError):
    """Unknown request exception, please create an issue feedback for this issue.

    """


class NotPageableError(BaseRequestError):
    """There is no previous or next page
    """


def raise_request_exception(response: Response) -> None:
    status_code = response.status_code
    if status_code == 200:
        pass
    elif status_code == 404:
        raise NotFoundError(response)
    elif 400 <= status_code < 500:
        raise BadRequestError(response)
    elif 500 <= status_code < 600:
        raise BadResponseError(response)
    else:
        raise UnknownRequestError(response)
