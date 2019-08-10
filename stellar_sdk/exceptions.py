class SdkError(Exception):
    """Base exception for all stellar sdk related errors
    """


class ValueError(ValueError, SdkError):
    """exception for all values related errors

    """


class TypeError(TypeError, SdkError):
    """exception for all type related errors

    """


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
