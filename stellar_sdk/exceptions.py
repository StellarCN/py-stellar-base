import binascii


class SdkError(Exception):
    def __init__(self, msg):
        super(SdkError, self).__init__(msg)


class ValueError(ValueError, SdkError):
    pass


class TypeError(TypeError, SdkError):
    pass


class BadSignatureError(SdkError):
    pass


class Ed25519PublicKeyInvalidError(SdkError):
    pass


class Ed25519SecretSeedInvalidError(SdkError):
    pass


class DecodeError(SdkError):
    pass


class MissingEd25519SecretSeedError(SdkError):
    pass


class MemoInvalidException(ValueError):
    pass


class AssetCodeInvalidError(ValueError):
    pass


class AssetIssuerInvalidError(ValueError):
    pass


class NoApproximationError(SdkError):
    pass


class SignatureExistError(SdkError):
    pass
