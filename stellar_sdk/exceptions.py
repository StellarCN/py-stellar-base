class StellarError(Exception):
    def __init__(self, msg):
        super(StellarError, self).__init__(msg)


class BadSignatureError(StellarError):
    pass


class Ed25519PublicKeyInvalidError(StellarError):
    pass


class Ed25519SecretSeedInvalidError(StellarError):
    pass


class DecodeError(StellarError):
    pass


class MissingEd25519SecretSeedError(StellarError):
    pass


class MemoInvalidException(StellarError, ValueError):
    pass


class AssetCodeInvalidError(StellarError):
    pass


class AssetIssuerInvalidError(Ed25519PublicKeyInvalidError):
    pass
