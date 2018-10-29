class StellarError(Exception):
    def __init__(self, msg):
        super(StellarError, self).__init__(msg)


class BadSignatureError(StellarError):
    pass


class AssetCodeInvalidError(StellarError):
    pass


class StellarAddressInvalidError(StellarError):
    pass


class StellarSecretInvalidError(StellarError):
    pass


class NoStellarSecretOrAddressError(StellarError):
    pass


class SequenceError(StellarError):
    pass


class ConfigurationError(StellarError):
    pass


class NoApproximationError(StellarError):
    pass


class HorizonError(StellarError):
    """A :exc:`HorizonError` that represents an issue stemming from
    Stellar Horizon.

    """
    def __init__(self, msg, status_code):
        super(HorizonError, self).__init__(msg)
        self.message = msg
        self.status_code = status_code


class HorizonRequestError(StellarError):
    """A :exc:`HorizonRequestError` that represents we cannot connect
    to Stellar Horizon.

    """
    pass


class SignatureExistError(StellarError):
    pass


class DecodeError(StellarError):
    pass


class NotValidParamError(StellarError):
    pass


class MnemonicError(StellarError):
    pass


class MissingSigningKeyError(StellarError):
    pass


class FederationError(Exception):
    """A :exc:`FederationError` that represents an issue stemming from
    Stellar Federation.

    """